# SocialNetworkCausalityWeb
Infer causal orders of users in social network(here we mean sina weibo) and extend it into a web project. The project is created to do some experiment about causality, which is my postgraduate research direction. Data is collected from sina weibo, including userid, weibo text. 

## Data collection
In this work, we use data of 21 users. At first, a spider is needed to spy pages which contain information we want and then persist them into database(here we use mongodb). Spider project isn't show here. 

## Data preprocessing
There're two types of data we want to put into the project. One is sequence data of user's activity and then topic vectors of user's text. 
### Sequence
Sequence is ...
### Topic vectors
...
2vec model training...

## Infer causal orders
### Transfer Entropy
..

### Local Transfer Entropy
...


## Result
The output is a causal network that is expressed as a matrix. By using this matrix, we can know causal orders of users. (Maybe some processing are required...)
