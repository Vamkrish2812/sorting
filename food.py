import pandas as pd
import ast

df=pd.read_csv("D:\\wiley_doc/RAW_interactions_cleaned.csv")
df1=pd.read_csv("D:\\wiley_doc/RAW_recipes_cleaned.csv")
df['date'] = pd.to_datetime(df['date'])
df1['submitted'] = pd.to_datetime(df1['submitted'])

# print(df.info())
# print(df1.info())



nutrition_cols = ['calories', 'total_fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates']
df1[nutrition_cols] = df1['nutrition'].str.strip('[]').str.split(',', expand=True).astype(float)

cal_conv=['total_fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates']

#df1[cal_conv]=((df1[cal_conv]/df1.calories)*100).astype(float)

for col in cal_conv:
    df1[col] = round((df1[col] / df1['calories']) * 100,2)

#print(df1[nutrition_cols].head())

df1['tags'] = df1['tags'].apply(ast.literal_eval)


df1 = df1.rename(columns={'id': 'recipe_id'})

df_total = pd.merge(df, df1, on='recipe_id')

#print(df_total.info())


# df_total['date'] = pd.to_datetime(df_total['date'])
# df_total['submitted'] = pd.to_datetime(df_total['submitted'])

# Calculate time difference in days

df_total['days_since_submission'] = (df_total['date'] - df_total['submitted']).dt.days


recipes_df = pd.DataFrame(df_total[['tags', 'rating','recipe_id']])


recipes_df = recipes_df.explode('tags')


tag_freq_df = recipes_df['tags'].value_counts().reset_index()
tag_freq_df.columns = ['tag', 'frequency']

tag_avg_rating_df = recipes_df.groupby('tags')['rating'].mean().reset_index()
tag_avg_rating_df.columns = ['tag', 'avg_rating']


tag_stats_df = pd.merge(tag_freq_df, tag_avg_rating_df, on='tag')
print(tag_stats_df.shape)

top_freq_threshold = tag_stats_df['frequency'].quantile(0.95)
top_rating_threshold = tag_stats_df['avg_rating'].quantile(0.95)
bottom_rating_threshold = tag_stats_df['avg_rating'].quantile(0.05)

top_freq_tags = tag_stats_df[tag_stats_df['frequency'] >= top_freq_threshold]
top_rating_tags = tag_stats_df[tag_stats_df['avg_rating'] >= top_rating_threshold]
bottom_rating_tags = tag_stats_df[tag_stats_df['avg_rating'] <= bottom_rating_threshold]

print("Top 5 Percentile Frequent Tags:")
print(top_freq_tags.head())

print("Top 5 Percentile Highest-Rated Tags:")
print(top_rating_tags.head())

print("Bottom 5 Percentile Highest-Rated Tags:")
print(bottom_rating_tags.head())
