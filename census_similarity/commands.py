import click

from census_similarity import techniques
from census_similarity.readers import read_columns


@click.command()
@click.option('--eps', type=float, default=0.10,
              help='similarity threshold (> 0.0, < 1.0)')
@click.option('--min-samples', type=int, default=2,
              help='minimum # to form a cluster')
@click.option('--technique', default='Jaccard', help='Similarity metric',
              type=click.Choice(['CharacterBag', 'Levenshtein', 'Jaccard',
                                 'Trigrams']))
@click.option('--field', default='name', help='field to cluster on',
              type=click.Choice(['name', 'description']))
def column_name(eps, min_samples, technique, field):
    """Print clusters of columns"""
    all_strs = [getattr(column, field) for column in read_columns()]

    groups = getattr(techniques, technique).cluster_groups(
        all_strs, eps, min_samples)
    for key, group in groups.items():
        print("\t", key, group)
