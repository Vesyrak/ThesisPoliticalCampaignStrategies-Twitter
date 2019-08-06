import pandas as pd

input_file = "input.csv"
count_file = "count.csv"

tags=[ 'party','family','relation','activity','past','attack']

input_df = pd.read_csv(input_file,header=None, names=['name', 'uid', 'date', 'mid', 'tweet_count', 'retweet_count', 'text', 'link','is_retweet','party','personalized','private','family','relation','activity','past','attack'])
count_df = pd.read_csv(count_file,header=None, names=['name','party','personalized','private','family','relation','activity','past','attack', 'total'])

nan_rows = input_df[input_df.isnull().T.any().T]
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(nan_rows)


count =0
error_df = pd.DataFrame()

def find_mistakes(df):
    global count, error_df
    tag_x =tags.copy()
    tag_y = tags.copy()
    for tag in tag_x:
        tag_y.remove(tag)
        for ty in tag_y:
            tag_list = df[(df[tag]==1) & (df[ty]==1) ]
            error_df=error_df.append(tag_list)
            count+=len(tag_list)
    tag_x =tags.copy()
    tag_x.remove('attack')
    tag_x.append('personalized')
    tag_y = tags.copy()
    tag_y.remove('attack')
    tag_y.append('personalized')
    for tag in tag_x:
        tag_y.remove(tag)
        for ty in tag_y:
            tag_list = df[(df[tag]==1) & (df[ty]==1) ]
            error_df=error_df.append(tag_list)
            count+=len(tag_list)


def find_names(df):
    return df['name'].unique()

def get_count(count_df, name):
    return count_df[count_df['name'].str.match(name)]['total']

def get_random_items(df, name, tag, count):
    name_list = df[df['name'].str.match(name)]
    tag_list = name_list[name_list[tag]==1]
    random_items = tag_list.sample(n=count)
    return random_items

def get_random_items_personalized(df, name, count):
    name_list = df[df['name'].str.match(name)]
    tag_list = name_list[(name_list['attack']==0) & (name_list['personalized']==1) ]
    random_items = tag_list.sample(n=count)
    return random_items


output_df = pd.DataFrame()

find_mistakes(input_df)

for name in find_names(input_df):
    if int(get_count(count_df, name)) < 60:
        random=input_df[input_df['name'].str.match(name)]
        output_df=output_df.append(random)
        pass
    else:
        count_p = int(count_df[count_df['name'].str.match(name)]["personalized"])
        random = get_random_items_personalized(input_df, name, count_p)
        output_df=output_df.append(random)

        for tag in tags:
            count = int(count_df[count_df['name'].str.match(name)][tag])
            random=get_random_items(input_df, name, tag, count)
            output_df=output_df.append(random)

print(output_df)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(error_df)
print(len(error_df))
print(len(output_df))

export_csv = output_df.to_csv (r'output.csv', index = None, header=True)
