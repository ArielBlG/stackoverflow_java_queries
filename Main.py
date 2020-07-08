import DataCollector
import CodeExtractor
import CodeParser


def Main():

    #the query we send to bigquery datasset, joining question and answer by id
    #filter the limit to 10000 - need better computer for more
    questions_query = """
                        SELECT pq.title,pq.body, com.body as answers_body
    FROM `bigquery-public-data.stackoverflow.posts_questions` as pq
    inner join `bigquery-public-data.stackoverflow.posts_answers` as com on pq.id = com.parent_id
    WHERE pq.tags LIKE '%java%' AND pq.tags NOT LIKE '%javascript%' AND pq.body LIKE '%<code>%' AND pq.body LIKE '%class%' 
         AND com.body LIKE '%<code>%' AND com.body LIKE '%class%'
    LIMIT 10000
                      """

    # creates the datacollector
    datacollector = DataCollector.dataCollector()
    datacollector.openclient()
    data_set = datacollector.getdataset(questions_query) #get the data set created from the bigquery dataset


    codeextractor = CodeExtractor.codeExtractor(data_set)

    #optional -- recevie a csv file instead of panda df
    # codeextractor = codeExtractor(%PATH%)
    codes = codeextractor.extractCodes()


    #parse the code
    codeparser = CodeParser.codeParser(codes)
    codeparser.parse_code()

if __name__ == "__main__":
    Main()