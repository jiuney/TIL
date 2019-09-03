# Amazon Book Review Analysis

아마존에서 판매하는 "A Game of Thrones: A Song of Ice and Fire, Book 1"의 customer review

```R
library(rvest)



# 한 페이지만 시범적으로 스크랩

url_a <- "https://www.amazon.com/product-reviews/B0001DBI1Q/ref=cm_cr_arp_d_paging_btm_next_"
url_p <- "?ie=UTF8&reviewerType=all_reviews&pageNumber="
page <- 2
url <- paste(url_a,page,url_p,page, sep = "")
url

htxt <- read_html(url)
htxt
review <- html_nodes(htxt, ".review-text-content")
review
review <- html_text(review)
review



# 1~5페이지만 시범적으로 스크랩

url_a <- "https://www.amazon.com/product-reviews/B0001DBI1Q/ref=cm_cr_arp_d_paging_btm_next_"
url_p <- "?ie=UTF8&reviewerType=all_reviews&pageNumber="

allReviews <- c()

for (page in 1:5){
  url <- paste(url_a, page, url_p, page, sep = "")
  htxt <- read_html(url)
  review <- html_nodes(htxt, ".review-text-content")
  review <- html_text(review)
  allReviews <- c(allReviews, review)
  print(page)
}

allReviews
write.table(allReviews, "project_review.txt")



# 1~500페이지 스크랩 (amazon에서 리뷰는 500페이지까지만 보인다)

url_a <- "https://www.amazon.com/product-reviews/B0001DBI1Q/ref=cm_cr_arp_d_paging_btm_next_"
url_p <- "?ie=UTF8&reviewerType=all_reviews&pageNumber="

allReviews <- c()

for (page in 1:500){
  url <- paste(url_a, page, url_p, page, sep = "")
  htxt <- read_html(url)
  review <- html_nodes(htxt, ".review-text-content")
  review <- html_text(review)
  allReviews <- c(allReviews, review)
  print(page)
}

allReviews
allReviews <- str_replace_all(allReviews, "[[:space:]]{2,}", "")    # 각 문단 뒤쪽의 공백 없애기

library(tm)
library(stringr)
library(SnowballC)

allReviews <- removeWords(allReviews, stopwords("SMART"))    # 불용어 없애기
allReviews <- str_replace_all(allReviews, "\\. ", " ")    # 마침표 없애기
allReviews <- str_replace_all(allReviews, "\\.", " ")
allReviews <- stemDocument(allReviews)    # 어근 추출



# afinn 감성 분석

library(tidytext)
get_sentiments("afinn")
AFINN <- data.frame(get_sentiments("afinn"))
AFINN

review.words <- str_extract_all(tolower(allReviews), boundary("word"))    # 소문자 통일, 단어 추출
review.words
review.word.table <- data.frame(table(unlist(review.words)))
review.word.table
colnames(review.word.table) <- c("word", "Frequency")
review.word.table

library(dplyr)
review.sentiment.table <- review.word.table %>% inner_join(AFINN, by="word")
review.sentiment.table

review.afinn <- review.sentiment.table %>% group_by(score) %>% summarise(freq=sum(Frequency))

library(ggplot2)
ggplot(data = review.afinn, aes(x=score, y=freq))+
  geom_col()+
  geom_text(aes(label=freq, vjust=-0.5))



# afinn 평점

sum(review.afinn$score*review.afinn$freq)/sum(review.afinn$freq)



# bing 감성 분석

BING <- data.frame(get_sentiments("bing"))
BING

review.bing.table <- review.word.table %>% inner_join(BING, by="word")
review.bing.table

# 참고: https://www.tidytextmining.com/sentiment.html
review.bing.table %>% 
  group_by(sentiment) %>%
  arrange(desc(Frequency)) %>% 
  top_n(10, Frequency) %>%
  ungroup() %>%
  mutate(word = reorder(word, Frequency)) %>%
  ggplot(aes(word, Frequency, fill = sentiment)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~sentiment, scales = "free_y") +
  labs(y = "Contribution to sentiment",
       x = NULL) +
  coord_flip()
  


# wordcloud (bing단어로)

library(wordcloud)
library(RColorBrewer)
review.bing.table %>% 
  anti_join(stop_words) %>% 
  with(wordcloud(words=word, 
                 freq=Frequency, 
                 max.words = 200,
                 col = brewer.pal(8, "Set1")))



# nrc 감성 분석

NRC <- data.frame(get_sentiments("nrc"))
NRC

review.nrc.table <- review.word.table %>% inner_join(NRC, by="word")
review.nrc.table

review.nrc.table %>% 
  count(word,sentiment, Frequency, sort=TRUE) %>%
  group_by(sentiment) %>% 
  top_n(10, Frequency) %>% 
  ungroup() %>%
  ggplot(aes(x=reorder(word,Frequency),y=Frequency,fill=sentiment)) + 
  geom_col(show.legend = FALSE) + 
  facet_wrap(~sentiment,scales="free") + 
  coord_flip()
```

