import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_datasets():
    facebook_df = pd.read_csv('facebook_dataset.csv', on_bad_lines='skip', low_memory=False)
    google_df = pd.read_csv('google_dataset.csv', on_bad_lines='skip', low_memory=False)
    website_df = pd.read_csv('website_dataset.csv', delimiter=';', on_bad_lines='skip', low_memory=False)
    return facebook_df, google_df, website_df

# Rename columns to standardize
def standardize_columns(df, source):
    if source == 'facebook':
        df.rename(columns={
            'name': 'company_name',
            'domain': 'domain_name',
            'categories': 'category',
            'phone': 'phone_number',
            'country_name': 'country',
            'region_name': 'region'
        }, inplace=True)
    elif source == 'google':
        df.rename(columns={
            'name': 'company_name',
            'domain': 'domain_name',
            'category': 'category',
            'phone': 'phone_number',
            'country_name': 'country',
            'region_name': 'region'
        }, inplace=True)
    elif source == 'website':
        df.rename(columns={
            'site_name': 'company_name',
            'root_domain': 'domain_name',
            's_category': 'category',
            'phone': 'phone_number',
            'main_country': 'country',
            'main_region': 'region',
            'main_city': 'city'
        }, inplace=True)
        
def clean_data(df):
    df['phone_number'] = df['phone_number'].fillna('').astype(str)
    df['phone_number'] = df['phone_number'].str.replace(r'\D', '', regex=True)
    df['company_name'] = df['company_name'].str.lower()
    df.fillna('', inplace=True)
        

def validate_data(df, name):
    description = df.describe(include='all')
    missing_values = df.isnull().sum()
    empty_values = (df == '').sum()
    description.to_csv(f'{name}_description.csv', index=True)
    missing_values.to_csv(f'{name}_missing_values.csv', index=True, header=['Missing Values'])
    empty_values.to_csv(f'{name}_empty_values.csv', index=True, header=['Empty Values'])
    print(f"Validation results saved for {name} dataset.")
    
# Merge datasets
def merge_datasets(facebook_df, google_df, website_df):
    merged_df = pd.merge(facebook_df, google_df, on='domain_name', how='outer', suffixes=('_facebook', '_google'))
    merged_df = pd.merge(merged_df, website_df, on='domain_name', how='outer', suffixes=('', '_website'))
    return merged_df

# View the merged data
def consolidate_data(merged_df):
    merged_df['category'] = merged_df['category_facebook'].combine_first(merged_df['category_google']).combine_first(merged_df['category'])
    merged_df['phone_number'] = merged_df['phone_number_facebook'].combine_first(merged_df['phone_number_google']).combine_first(merged_df['phone_number'])
    merged_df['country'] = merged_df['country_facebook'].combine_first(merged_df['country_google']).combine_first(merged_df['country'])
    merged_df['region'] = merged_df['region_facebook'].combine_first(merged_df['region_google']).combine_first(merged_df['region'])
    merged_df['city'] = merged_df['city_facebook'].combine_first(merged_df['city_google']).combine_first(merged_df['city'])
    return merged_df

def drop_redundant_columns(merged_df):
    merged_df.drop(columns=['category_facebook', 'category_google', 'phone_number_facebook', 'phone_number_google', 
                            'country_facebook', 'country_google', 'region_facebook', 'region_google', 
                            'city_facebook', 'city_google'], inplace=True)
    
def visualize_data(merged_df):
    plt.figure(figsize=(12, 6))
    
    sns.countplot(data=merged_df, x='category', order=merged_df['category'].value_counts().index)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('category_distribution.png')
    plt.show()
    
    plt.figure(figsize=(12, 6))
    sns.countplot(data=merged_df, x='phone_number', order=merged_df['phone_number'].value_counts().index)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('phone_number_distribution.png')
    plt.show()
    
def main():
    # read dataset
    facebook_df, google_df, website_df = read_datasets()
    
    # inspect the datasets
    print("Facebook dataset")
    print(facebook_df.head())
    print("Google dataset")
    print(google_df.head())
    print("Website dataset")
    print(website_df.head())
    
    # standardize columns
    standardize_columns(facebook_df, 'facebook')
    standardize_columns(google_df, 'google')
    standardize_columns(website_df, 'website')
    
    # clean data
    clean_data(facebook_df)
    clean_data(google_df)
    clean_data(website_df)
    
    # validate data
    validate_data(facebook_df, 'facebook')
    validate_data(google_df, 'google')
    validate_data(website_df, 'website')
    
    # merge datasets
    merged_df = merge_datasets(facebook_df, google_df, website_df)
    merged_df = consolidate_data(merged_df)

    # drop redundant columns
    drop_redundant_columns(merged_df)

    # save the merged dataset
    merged_df.to_csv('merged_companies_dataset.csv', index=False)

    # visualize_data(merged_df)

if __name__ == "__main__":
    main()