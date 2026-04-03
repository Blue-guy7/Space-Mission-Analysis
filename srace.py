import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")
plt.rcParams['font.size'] = 12

def clean_space_data(filepath):
    df = pd.read_csv(filepath)
    df = df.drop(columns=['Unnamed: 0.1', 'Unnamed: 0'], errors='ignore')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True)
    df['Year'] = df['Date'].dt.year
    df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(',', '', regex=False), errors='coerce')
    df['Country'] = df['Location'].apply(lambda x: str(x).split(',')[-1].strip())
    
    region_map = {
        'Kazakhstan': 'USSR/Russia', 'Russian Federation': 'USSR/Russia',
        'USA': 'USA', 'China': 'China', 'France': 'Europe', 'India': 'India'
    }
    df['Region'] = df['Country'].map(region_map).fillna('Other')
    
    return df
df= clean_space_data('mission_launches.csv')
space_race = df[(df['Year'] >= 1957) & (df['Year'] <= 1975)].copy()
sr_counts = space_race.groupby(['Year', 'Region']).size().unstack(fill_value=0)

plt.figure(figsize=(14, 7))
cols_to_plot = [c for c in ['USA', 'USSR/Russia'] if c in sr_counts.columns]
sr_counts[cols_to_plot].plot(kind='bar', ax=plt.gca(), width=0.8, color=['#1f77b4', '#d62728'])

plt.title('The Cold War Space Race: USA vs USSR (1957-1975)')
plt.ylabel('Annual Launch Volume')
plt.tight_layout()
plt.savefig('space_race_comparison.png')

top_countries = df['Country'].value_counts().nlargest(10).index
success_rate = (
    df[df['Country'].isin(top_countries)]
    .groupby('Country')['Mission_Status']
    .apply(lambda x: (x == 'Success').mean() * 100)
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
sns.barplot(
    x=success_rate.values, 
    y=success_rate.index, 
    hue=success_rate.index, 
    palette='magma', 
    legend=False
)
plt.title('Engineering Reliability: Mission Success Rate (%)')
plt.xlabel('Success Percentage')
plt.tight_layout()
plt.savefig('success_rate_by_country.png')