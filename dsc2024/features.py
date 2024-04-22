from typing import Callable, Tuple, Dict

import networkx as nx
import pandas as pd
import numpy as np
from PIL import Image as PIL_Image

from torch import nn
from torchvision.models import ViT_B_16_Weights
from torchvision.models.vision_transformer import vit_b_16
import torch


def insert_graph_measure(df: pd.DataFrame, measure_dict: Dict, name_measure: str, directed: bool = True):
    """
    Inserts graph measures into the DataFrame based on the provided measure dictionary.

    Args:
        df (pd.DataFrame): DataFrame containing 'origem' and 'destino' features.
        measure_dict (Dict): Dictionary with edge measures.
        name_measure (str): Name of the measure to insert.
        directed (bool, optional): Whether the graph is directed. Defaults to True.

    Returns:
        pd.DataFrame: DataFrame with the inserted measure column.
    """

    df[name_measure] = pd.Series(dtype=float)
    for edge, measure_value in measure_dict.items():
        if directed:
            origem, destino = edge
            mask = (df.origem == origem) & (df.destino == destino)
            df.loc[mask, name_measure] = measure_value
        else:
            origem, destino = edge
            mask = (df.origem == origem) & (df.destino == destino) | (df.origem == destino) & (df.destino == origem)
            df.loc[
                mask,
                name_measure,
            ] = measure_value


def generate_graph_features(df: pd.DataFrame):
    """
    Generates graph features for the given DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with 'origem' and 'destino' features.

    Returns:
        pd.DataFrame: DataFrame with additional graph features.
    """

    arcs = list(zip(df.origem, df.destino))

    arcs_freq = {x: arcs.count(x) for x in set(arcs)}

    G = nx.DiGraph()
    G_topo = nx.Graph()

    edges = [tuple(list(tup) + [val])
             for tup, val in zip(arcs_freq.keys(), arcs_freq.values())]

    G.add_weighted_edges_from(edges)
    G_topo.add_weighted_edges_from(edges)

    insert_graph_measure(df, nx.edge_betweenness_centrality(G), "betwenness")
    insert_graph_measure(
        df, nx.edge_current_flow_betweenness_centrality(G_topo), "flow_betweenness_topo", directed=False
    )

    df["edge_connectivity"] = pd.Series(dtype=float)
    df["deg_diff"] = pd.Series(dtype=float)

    for origem, destino, weight in edges:
        connec = nx.algorithms.connectivity.local_edge_connectivity(G, destino, origem)
        degdiff = G.degree(destino) - G.degree(origem)
        df.loc[(df.origem == origem) & (df.destino == destino), "edge_connectivity"] = connec
        df.loc[(df.origem == origem) & (df.destino == destino), "deg_diff"] = degdiff

    gmatrix = nx.google_matrix(G)
    df["gmatrix"] = pd.Series(dtype=float)

    nodes = list(G.nodes())
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            origem = nodes[i]
            destino = nodes[j]
            df.loc[(df.origem == origem) & (df.destino == destino), "gmatrix"] = gmatrix[i][j]

    return df


def graph_features_testdata(df_test: pd.DataFrame, df_train: pd.DataFrame):
    """
    Generates graph features for the test dataset based on measures computed from the train dataset.

    Args:
        df_test (pd.DataFrame): Test dataset with 'origem' and 'destino' features.
        df_train (pd.DataFrame): Train dataset with computed graph measures.

    Returns:
        pd.DataFrame: Test dataset with additional graph features.
    """

    # FIXME(@jorge, @lerax): sex 19 abr 2024 16:25:27
    # Translate the whole code to a format of Custom transformation of sklearn
    # ref: https://www.andrewvillazon.com/custom-scikit-learn-transformers/
    # store internal graph with measures at transformation.fit and apply then
    # based on (origem, destino) with transformation.transform
    train_measures = {}

    for _, row in df_train.iterrows():
        edge_key = (row["origem"], row["destino"])
        train_measures[edge_key] = {
            "betwenness": row["betwenness"],
            "flow_betweenness_topo": row["flow_betweenness_topo"],
            "edge_connectivity": row["edge_connectivity"],
            "deg_diff": row["deg_diff"],
            "gmatrix": row["gmatrix"],
        }

    for _, row in df_test.iterrows():
        edge_key = (row["origem"], row["destino"])
        if edge_key in train_measures:
            df_test.loc[_, "betwenness"] = train_measures[edge_key]["betwenness"]
            df_test.loc[_, "flow_betweenness_topo"] = train_measures[edge_key]["flow_betweenness_topo"]
            df_test.loc[_, "edge_connectivity"] = train_measures[edge_key]["edge_connectivity"]
            df_test.loc[_, "deg_diff"] = train_measures[edge_key]["deg_diff"]
            df_test.loc[_, "gmatrix"] = train_measures[edge_key]["gmatrix"]
        else:
            df_test.loc[_, "betwenness"] = None
            df_test.loc[_, "flow_betweenness_topo"] = None
            df_test.loc[_, "edge_connectivity"] = None
            df_test.loc[_, "deg_diff"] = None
            df_test.loc[_, "gmatrix"] = None

    return df_test


def load_transformer_feature_extractor() -> Tuple[Callable[[PIL_Image.Image], torch.Tensor], nn.Module]:
    """
    Load the Vision Transformer (ViT) model and its preprocessing function.

    Returns:
        Tuple[Callable[[PIL_Image.Image], torch.Tensor], nn.Module]:
        A tuple containing the preprocessing function and the ViT model.
    """
    vit = vit_b_16(weights=ViT_B_16_Weights.DEFAULT)
    preprocessing = ViT_B_16_Weights.DEFAULT.transforms()
    return preprocessing, vit


def feature_extraction_from_image(
    img: PIL_Image.Image,
    preprocessing: Callable[[PIL_Image.Image], torch.Tensor],
    vit: nn.Module
) -> np.ndarray:
    """
    Embed an image using a Vision Transformer (ViT) model.

    Args:
        img (PIL_Image.Image): The input image to be embedded.
        preprocessing (Callable[[PIL_Image.Image], torch.Tensor]): A function for preprocessing the image.
        vit (nn.Module): The Vision Transformer model.

    Returns:
        np.ndarray: The embedded representation of the input image.
    """
    tensor = preprocessing(img).unsqueeze(0)
    feats = vit._process_input(tensor)
    batch_class_token = vit.class_token.expand(tensor.shape[0], -1, -1)
    feats = torch.cat([batch_class_token, feats], dim=1)
    feats = vit.encoder(feats)
    feats = feats[:, 0]
    return np.array(torch.flatten(feats).detach().numpy())
