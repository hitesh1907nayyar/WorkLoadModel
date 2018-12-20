FROM continuumio/anaconda3:5.0.0
#MAINTAINER UNP, https://unp.education
COPY ./flask_demo /usr/local/python/
EXPOSE 4200
WORKDIR /usr/local/python/
CMD python Python_Script_Load_Per_Week_Date_as_input.py
