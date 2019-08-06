from twitter_scraper import get_tweets
import csv
from datetime import datetime
import sys

user_dict = {
        "Bart_DeWever": "1.5.1",
        "LiesbethHomans": "1.5.2",
        "AnnickDeRidder": "1.5.4",
        "FPerdaens": "1.5.7",
        "PaulCordy": "1.5.8",
        "manuelavanwerde": "1.5.10",
        "philippemuyters": "1.5.33",
        "KVDHeuvel_VP": "1.3.1",
        "KatrienSchryver": "1.3.3",
        "orry_vdw": "1.3.4",
        "Dirk_de_Kort": "1.3.6",
        "BartSomers": "1.4.1",
        "SihameElk": "1.4.2",
        "wfschiltz": "1.4.3",
        "carogennez": "1.2.1",
        "MeyremAlmaci": "1.1.1",
        "ImadeAnnouri": "1.1.2",
        "WouterVanBesien": "1.1.33",
        "FDW_VB": "1.6.1",
        "claesbart": "1.6.2",
        "BenWeyts":"2.5.1",
        "lorinparys123":"2.5.3",
        "PietDeBruyn":"2.5.4",
        "inez_deconinck":"2.5.5",
        "allessiaclaes":"2.5.6",
        "ElkeWouters3":"2.5.7",
        "Petervanrompuy":"2.3.1",
        "BrouwersKarin":"2.3.2",
        "JelleWout":"2.3.5",
        "RuttenGwendolyn":"2.4.1",
        "Mauritsvdr":"2.4.2",
        "jo_dero":"2.4.4",
        "IrinaDeKnop":"2.4.5",
        "RikDaems":"2.4.20",
        "katiasegers":"2.2.2",
        "anmoerenhout":"2.1.1",
        "ChrisSteenwegen":"2.1.2",
        "KlaasSlootmans":"2.6.1",
        "MaertensBert":"3.5.1",
        "VreeseMaaike":"3.5.2",
        "axel_ronse":"3.5.3",
        "WilfriedVdaele":"3.5.4",
        "DanielleTJonck":"3.5.22",
        "crevits":"3.3.1",
        "BartDochy":"3.3.2",
        "martine_menen":"3.3.3",
        "LoesVandromme":"3.3.4",
        "F3lixDeClerck":"3.3.22",
        "Barttommelein":"3.4.1",
        "emmilytalpe":"3.4.2",
        "MercedesVVolcem":"3.4.3",
        "FrancescoFV":"3.4.4",
        "LambrechtAnnick":"3.2.1",
        "steve_vdb":"3.2.2",
        "maximveys":"3.2.3",
        "philippedecoene":"3.2.22",
        "JeremieVaneeckh":"3.1.1",
        "BelindaMTL":"3.1.2",
        "DavidWemel":"3.1.3",
        "BartCaron":"3.1.22",
        "StefaanSintobin":"3.6.1"
        "Vera_Celis":"1.5.32",
        "driescouckuyt" : "3.2.4"
        }

header = ["Naam","Plaats ID", "Tijdstip", "Unieke ID", "likes", "retweets", "tekst", "URL" , "is_Retweet"]

def tweet_to_csv(output_file,name,  tweet):
    row = [name, get_person_place_id(name), tweet['time'], generate_tweet_babs_id(tweet['time']), tweet['likes'], tweet['retweets'], tweet['text'], generate_url(tweet['tweetId']), int(tweet['isRetweet'])]
    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(row)
    output_file.flush()

def generate_tweet_babs_id( tweet_time):
    with open('output.csv', mode='r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',')
        count = 1
        date = get_date(tweet_time)
        next(csv_reader, None)
        header = True
        for row in csv_reader:
            if len(row)<=3 :
                header=False
                continue
            user_id = row[3]
            user_time, user_cnt = user_id.split("x")
            if date == user_time and count <= int(user_cnt):
                count= int(user_cnt)+1
        return str(date)+"x"+str(count)

def generate_url(tweet_id):
    return "https://twitter.com/naam/status/"+tweet_id

def get_person_place_id(name):
    return user_dict.get(name, "-")

def get_date(tweet_time):
    return tweet_time.strftime("%d%m%Y")


with open('output.csv', mode='a') as output_file:
    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)
    i = 0
    for politieker in user_dict:
        tweet_count = 0
        for tweet in get_tweets(politieker, pages=10):
            if "2019-05-26" >= tweet['time'].strftime('%Y-%m-%d') and tweet['time'].strftime('%Y-%m-%d') >= "2019-04-01":
                tweet_to_csv(output_file, politieker, tweet)
                tweet_count+=1
        writer.writerow([politieker, tweet_count])

output_file.close()

