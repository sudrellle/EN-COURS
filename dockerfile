FROM PYTHON
COPY /app .
COPY ./requirement.txt /tmp/requirement.txt
RUN pip install -r /tmp/requiremt.txt
EXPOSE 
CMD ["streamlit",""]
