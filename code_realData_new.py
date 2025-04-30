try:
    import numpy as np
except ImportError:
    print("Trying to install required module: numpy \n")
    os.system('python3 - m pip install numpy')
    import numpy as np

try:
    import re
except ImportError:
    print("Trying to install required module: re \n")
    os.system('python3 - m pip install re')
    import re

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Trying to install required module: matplotlib \n")
    os.system('python3 - m pip install matplotlib')
    import matplotlib.pyplot as plt

try:
    import networkx as nx
except ImportError:
    print("Trying to install required module: networkx \n")
    os.system('python3 - m pip install networkx')
    import networkx as nx

try:
    import glob
except ImportError:
    print("Trying to install required module: glob \n")
    os.system('python3 - m pip install glob')
    import glob

import random
import time
import csv
from datetime import datetime
import os
import pandas as pd

print('Loading data...')

# common folders
FolderFollowers = '/Followers'
FolderFollowings = '/Followings'
FolderHistory = '/History'
FolderProfile = '/Profile'
FolderRetweeters = '/Retweeters'
FolderTweets = '/Tweets'

# now check with the folder approach
user_folders = glob.glob('./Test/RetweetCollection/*')
for folder in user_folders:

    # Followers Path
    FolderFollowersComplete = folder + FolderFollowers
    FolderFollowingsComplete = folder + FolderFollowings
    FolderHistoryComplete = folder + FolderHistory
    FolderProfileComplete = folder + FolderProfile
    FolderRetweetersComplete = folder + FolderRetweeters
    FolderTweetsComplete = folder + FolderTweets
    # if any of the folder are empty not considering the tweet
    if (len(os.listdir(FolderFollowersComplete)) == 0 or len(os.listdir(FolderFollowingsComplete)) == 0 or
            len(os.listdir(FolderHistoryComplete)) == 0 or len(os.listdir(FolderProfileComplete)) == 0 or
            len(os.listdir(FolderRetweetersComplete)) == 0 or len(os.listdir(FolderTweetsComplete)) == 0):
        #print("Directory is empty")
        pass
    else:
        #print("Directory is not empty")
        # from here the loading will start

        #get the folder ids should be same for the other folders
        get_folder_ids_followers = glob.glob(FolderFollowersComplete + '/*')
        folder_id_list = []
        for get_folder_id in get_folder_ids_followers:
                tmp = get_folder_id.split('/')
                folder_id_list.append(tmp[-1])
        
        # loop through each of the 
        for folder_id in folder_id_list:

            FollowersID = []
            #followers_path = data_path + '/Followers/1427639234576490506'
            followers_path = FolderFollowersComplete + '/' + folder_id
            files = os.listdir(followers_path)
            i = 0
            for file in files:
                position = followers_path + '/' + file
                with open(position, "r",encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:            
                        FollowersID.append([i,file.replace('_followers_.txt',''),line.replace('\n','')])
                        i = i+1
                    f.close()
            FollowersID = np.array(FollowersID)


            FollowingID = []
            #followings_path = data_path + '/Followings/1427639234576490506'
            followings_path = FolderFollowingsComplete + '/' + folder_id
            files = os.listdir(followings_path)
            i = 0
            for file in files:
                position = followings_path + '/' + file
                with open(position, "r",encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:        
                        FollowingID.append([i,file.replace('_following_.txt',''),line.replace('\n','')])
                        i = i+1
                    f.close()
            FollowingID = np.array(FollowingID)


            RetweeterHistory = pd.DataFrame()
            #history_path = data_path + '/History/1427639234576490506'
            history_path = FolderHistoryComplete + '/' + folder_id
            files = os.listdir(history_path)
            i = 0
            for file in files:
                position = history_path + '/' + file
                df = pd.read_excel(position)
                RetweeterHistory = pd.concat([RetweeterHistory,df])
            RetweeterHistory = RetweeterHistory.reset_index().values


            MergedRetweets = pd.DataFrame()
            #Retweeters_path = data_path + '/Retweeters/1427639234576490506'
            Retweeters_path = FolderRetweetersComplete + '/' + folder_id
            files = os.listdir(Retweeters_path)
            for file in files:
                position = Retweeters_path + '/' + file
                df = pd.read_excel(position)
                MergedRetweets = pd.concat([MergedRetweets,df])
            MergedRetweets = MergedRetweets.reset_index().values
            print('Data loading is complete')   


            print('Calculating')
            poster_tweet = pd.DataFrame()
            #poster_path = data_path + '/Tweets/BarackObama_tweets_.xlsx'
            get_file = glob.glob(FolderTweetsComplete + '/' + folder_id + '/*.xlsx')
            for poster_path in get_file:
                poster_tweet = pd.read_excel(poster_path)
                poster_tweet.iloc[0,0] = str(pd.to_datetime(poster_tweet.iloc[0,0]))
                poster_tweet = poster_tweet.reset_index().values


#follower count
fav = []
for f in range(0,len(MergedRetweets[:,6])):
    fav.append(len(np.where(FollowersID[:,1] == MergedRetweets[f,6])[0]))
fav=np.asarray(fav)


#create list to store user who retweet, who post,retweet time, tweet text, and retweet user id
rt_hst =  RetweeterHistory
who_post = []
# for loop
for i in range(0,len(rt_hst)):
    # get tweet with retweet entity
    twit = rt_hst[i,3]
    # name of retweeted user
    who_post_str = "".join(re.findall(r"RT @(.+?):",twit))
    who_post.append(who_post_str)


cas_cad = np.vstack((MergedRetweets[:,6],MergedRetweets[:,1])).T
cas_cad = cas_cad[::-1] ##fixed
poster_info = np.vstack((poster_tweet[:,5],poster_tweet[:,1])).T
#poster_id = "{:.6e}".format(int(poster_tweet[0, 4]))
poster_id = str(poster_tweet[0, 4])
cs_cad = np.vstack((poster_info, cas_cad))
rewtr_id = MergedRetweets[:, 5]
fol_lst = FollowersID

infected = cs_cad[:,0]
folwing = FollowingID
following_poster = folwing[np.where(folwing[:,2] == poster_id)[0],1]


fol = []
fl1 = []
for i in range(0,len(infected)):
    if infected[i] in following_poster:
        fl1.append(i)
fol.append(fl1)


for i in range(1,len(infected)):
    rewtr_index = []
    
    ff = np.where(infected[i] == fol_lst[:,1] )[0]
    if len(ff) != 0:
        #print(i)
        iidd = fol_lst[ff,2]
        for j in range(0,len(rewtr_id)):
            if str(rewtr_id[j]) in iidd:
                rewtr_index.append(j)
                
        fol.append(rewtr_index)
    else:
        fol.append([])


#collect history
hist_list = [[] for i in range(len(infected))]
for k in range(0,len(infected)):
#for k in range(0,1):
    ht = [[] for i in range(len(infected))]
    hist = [[] for i in range(len(infected))]
    for i in range(0,len(infected)):
        if i>k:
            ww = np.where(who_post == infected[i])[0]
            rr = np.where(rt_hst[ww,5] ==infected[i])[0]
            tim = rt_hst[:,1]
            ht[i] = tim[ww[rr]]
            if len(ht[i]) == 0:
                #if there is no retweeted occured
                hist[i] = []
            else:
                histo = np.where(cs_cad[k,1] > ht[i])[0]
                
                if (len(histo) != 0):
                    #if any retweet happens before kth post
                    hist[i] = np.sort(ht[i][histo])  #retweets times in ordered manner
                else:
                    #if no retweet happens before kth post
                    hist[i] = []
                    
    hist_list[k] = hist
    

nd = [[] for i in range(len(infected))]
for i in range(1,len(infected)):
    nd[i] = np.where(rt_hst[:,5] == infected[i])[0]

content = [[] for i in range(len(infected))]
for i in range(1,len(infected)):
    content[i] = rt_hst[nd[i],3]
content[0] = rt_hst[np.where(np.asarray(who_post) == infected[0])[0],3]   


follower = fol
cascades = cs_cad
external = infected[0]
history = hist_list


# implement algorithm2. Caculate P_uv
def edge_prob(temp, B, E, J, F_uv, gamma_star):
    
    if(E==0):
        prob_uv = B*(1-E)* J * temp * F_uv * gamma_star
        return prob_uv
    if(E==1):
        if (F_uv==1):
            prob_uv = B * E * J * temp * F_uv * gamma_star
            return prob_uv
        if (F_uv==0):
            prob_uv = B * E * J * temp * (1 - F_uv)
            return prob_uv
    else:
        return 0


def Jaccard(content_u, content_v):
    x = str(content_u).split(" ")
    y = str(content_v).split(" ")
    J = 0
    intersection = len(set(x).intersection(set(y)))
    union = len(set(x)) + len(set(y)) - intersection
    J = intersection / union
    if (J < 0.001):
        J = 0.001
    return J 


def hawkes(hstry):
    arrivals=np.array(hstry)  #list to array
    #gamma_star=0.001
    #gamma_sta= None
    n = len(arrivals)
    #if(n>1):
    for l in range(0,10):
        gamma_star = np.zeros(10)
        store = np.zeros((100,3))
        k=0
        for i in range(0,10):
            alpha_i = random.uniform(0,0.1)
            #alpha_i = 0.1
            for j in range(0,10):
                beta_i = random.uniform(0,0.1)
                #beta_i = 0.1
                term_2 = sum(alpha_i/beta_i*(np.exp( -beta_i * (arrivals[n-1] - arrivals)) - 1))

                Ai = [sum(np.exp( -beta_i * (arrivals[z]- arrivals[0:z]))) for z in range(1,n)]

                term_3 = sum(np.log( alpha_i * np.array(Ai)))
                store[k,:] = (alpha_i,beta_i,term_2 +term_3)
                #print(k)
                k=k+1

        ll = np.where(store[:,2]==max(store[:,2]))[0]
        alpha = store[ll,0]
        beta=store[ll,1]
        Ai = sum(np.exp( -beta * (arrivals[n-1]- arrivals[0:(n-1)])))  
        gamma_star[l] = alpha*Ai

    return(np.mean(gamma_star))


def weigth_matrix(nodes,timec,external,follower,content,history):
    #j=1
    weight=[]
    srcnd = []
    dstnd = []
    J_uv = []
    gamma_uv =[]
    gamma_star = 0.001
    total_td = []
    sr_name = []
    ds_name = []
    for k in range(len(timec)):
        for i in range(len(timec)):
            if i<k:
                timec_k = timec[k][:19]
                timec_i = timec[i][:19]

                total_td.append((datetime.strptime(timec_k, '%Y-%m-%d %H:%M:%S')- datetime.strptime(timec_i, '%Y-%m-%d %H:%M:%S')).total_seconds()/60)
    median_td = np.median(total_td)                       
    
    for k in range(0,len(nodes)):
        for i in range(0,len(nodes)):
            if i<k:
                timec_k = timec[k][:19]
                timec_i = timec[i][:19]
                diffs = (datetime.strptime(timec_k, '%Y-%m-%d %H:%M:%S')- datetime.strptime(timec_i, '%Y-%m-%d %H:%M:%S')).total_seconds()/60/median_td
                if diffs == 0:
                    temp = 0
                if diffs !=0:
                    #dif = np.abs(np.log(diffs))
                    dif = np.log(diffs)
                if np.exp(-dif) == 0:
                    temp = np.exp(-700)
                if np.exp(-dif) != 0:
                    temp = np.exp(-dif)
                sig_sq = (1 / (2 * len(fav))) * np.mean(np.power(fav,2)) #rayleigh parameter
                B = (fav[i] / sig_sq) * np.exp(-((np.power(fav[i],2)) / (2 * sig_sq))) #Rayleigh Distribution
                
                if nodes[i] in external:
                    E = 1
                else:
                    E = 0 
                
                if k in follower[i]:
                    F_uv = 1
                else:
                    F_uv = 0
                
                if (len(content[i]) != 0 and len(content[k]) != 0):
                    J = Jaccard(content[i],content[k])
                if (len(content[i]) == 0 or len(content[k]) == 0):
                    J = 0.001
                    
                if F_uv != 0:
                    if len(history[i][k]) != 0:
                        cur_time = datetime.timestamp(datetime.strptime(timec[i],'%Y-%m-%d %H:%M:%S+%z'))
                        for j in range(0,len(history[i][k])):
                            history[i][k][j] = datetime.timestamp(datetime.strptime(history[i][k][j],'%Y-%m-%d %H:%M:%S+%z'))
                        
                        hst = np.sort(np.hstack((history[i][k],cur_time)))  
                        gamma_star = hawkes(hst)
                    else:
                        gamma_star = 0.001
                weight.append(edge_prob(temp, B, E, J, F_uv, gamma_star)) 
                J_uv.append(J)
                gamma_uv.append(gamma_star)
                srcnd.append(nodes[i])
                dstnd.append(nodes[k])
                
    return(np.vstack((srcnd, dstnd, weight, J_uv, gamma_uv)).T)


arcs = []
nodes = cascades[:, 0]
timec = cascades[:, 1]
start_time = time.time()

arcs = weigth_matrix(nodes, timec, external, follower, content, history)
end_time = time.time()

total_time = end_time - start_time
print('Total run time is '+ round(str(total_time), 2) + 'sec')

aa = np.unique(arcs[:, 1])
for i in range(0,len(aa)):
    bb = np.where(arcs[:, 1] == aa[i])[0]
    cc = np.argmax(arcs[bb, 2].astype(np.float64))
    arcs[np.delete(bb,cc),2] = 0


zero_weigth = np.where(arcs[:, 2] == '0')[0]
index = np.arange(0, len(arcs))
network = arcs[np.delete(index,zero_weigth), :]
network_df = pd.DataFrame(network,columns = ['source node', 'destination node', 'weight', 'J_uv', 'gamma_uv'])
network_df.to_excel(r'Result.xlsx')
print('The result is saved')

# plot
print('The graph is creating.')
#A = network[:,0:2].astype(int)
A = network[:,0:2]
df = pd.DataFrame(A, columns = ['source','target'])


G = nx.from_pandas_edgelist(df, 'source', 'target')
pos = nx.spring_layout(G)
plt.rcParams['figure.figsize'] = (20.0, 18.0)
nx.draw(G,pos,node_size = 150,alpha =0.9,with_labels = True)
plt.savefig("result.png",dpi = 500)
print('The graph is saved.')
