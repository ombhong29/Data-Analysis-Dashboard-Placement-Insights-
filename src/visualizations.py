# # src/visualizations.py
# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set_theme(style='whitegrid', palette='muted')

# def plot_top_companies(df_placed):
#     top = df_placed['company'].value_counts().head(10)
#     fig, ax = plt.subplots(figsize=(8,4))
#     sns.barplot(x=top.values, y=top.index,
#                 palette='Blues_r', ax=ax)
#     ax.set_xlabel('Students hired')
#     ax.set_title('Top hiring companies')
#     plt.tight_layout()
#     return fig

# def plot_skill_demand(skill_df):
#     fig, ax = plt.subplots(figsize=(8,4))
#     sns.barplot(data=skill_df.head(10),
#                 x='count', y='skill',
#                 palette='Greens_r', ax=ax)
#     ax.set_title('Most in-demand skills')
#     plt.tight_layout()
#     return fig

# src/visualizations.py
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style='whitegrid', palette='muted')

def plot_top_companies(df_placed):
    top = df_placed['company'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8,4))
    sns.barplot(x=top.values, y=top.index,
                palette='Blues_r', ax=ax)
    ax.set_xlabel('Students hired')
    ax.set_title('Top hiring companies')
    plt.tight_layout()
    return fig


def plot_skill_demand(skill_df):
    fig, ax = plt.subplots(figsize=(8,4))
    sns.barplot(data=skill_df.head(10),
                x='count', y='skill',
                palette='Greens_r', ax=ax)
    ax.set_title('Most in-demand skills')
    plt.tight_layout()
    return fig

def plot_package_distribution(df):
    fig, ax = plt.subplots(figsize=(8,4))

    # find package column automatically
    pkg_col = [c for c in df.columns if "package" in c.lower()][0]

    sns.histplot(df[pkg_col], bins=10, kde=True, ax=ax)

    ax.set_title("Package Distribution")
    ax.set_xlabel("Package (LPA)")
    plt.tight_layout()
    return fig


def plot_cgpa_vs_package(df):
    fig, ax = plt.subplots(figsize=(8,4))

    pkg_col = [c for c in df.columns if "package" in c.lower()][0]

    sns.scatterplot(
        data=df,
        x="cgpa",
        y=pkg_col,
        hue="branch",
        ax=ax
    )

    ax.set_title("CGPA vs Package")
    plt.tight_layout()
    return fig