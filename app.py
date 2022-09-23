from flask import Flask, render_template, request,jsonify
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urReq
import requests

app = Flask(__name__)

@app.route('/',methods=['GET'])

def home():
    return render_template("index.html")


@app.route('/review',methods=['GET','POST'])

def index():
    if request.method=='POST':
        try:
            print('ki')
            searchitem=request.form['content'].replace(" ","")
            print(searchitem)
            flip_url="https://www.flipkart.com/search?q="+ searchitem
            print(flip_url)
            link=urReq(flip_url)
            print(link)
            html_page=link.read()
            link.close()
            beauty=bs(html_page,'html.parser')



            bigbox = beauty.find_all("div", {"class": "_1AtVbE col-12-12"})
            print(len(bigbox))

            product="https://www.flipkart.com" + bigbox[4].div.div.div.a['href']
            print(product)
            pro=requests.get(product)
            print(pro)
            pro.encoding='utf-8'
            prod_html = bs(pro.text, "html.parser")
            print(len(prod_html))

            commentboxes=prod_html.find_all('div', {"class": "_16PBlm"})


            filename='searchitem'+'.csv'
            fw=open(filename,'w')
            headers="Product,Price,Customer Name,Rating,Heading,Comment\n"
            fw.write(headers)
            review=[]
            for i in commentboxes:
                try:
                    name=i.div.div.find_all('p',{'class':'_2sc7ZR _2V5EHH'})[0].text
                    print (name)
                except:
                    name="No Name"



                try:
                    price = prod_html.find_all('div', {'class': '_30jeq3 _16Jk6d'})[0].text
                    print(price)
                except:
                    price = "No price available"
                try:

                    rating = i.div.div.div.div.text
                    print(rating)


                except :
                    rating = 'No Rating'


                try:

                    commentHead = i.div.div.find_all('p',{'class':'_2-N8zT'})[0].text
                    print(commentHead)
                except:
                    commentHead = 'No Comment Heading'

                try:
                    comtag = i.div.div.find_all('div', {'class': ''})[0].div.text

                    print(comtag)
                except Exception as e:
                    print("Exception while creating dictionary: ", e)

                mydict={"Product": searchitem,"Price":price, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": comtag}
                print(mydict)

                review.append(mydict)
            return render_template('result.html', review=review[0:(len(review)-1 )])

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

        return render_template('result.html')

    else:
        return render_template('index.html')




if __name__=="__main__":
    app.run(port=8000,debug=True)