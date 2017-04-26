# The MIT License (MIT)

#Copyright (c) 2016 - 2017 Alberto Sanchez de la Cruz

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import http.client
import http.server
import json
import socketserver

class OpenFDAClient():
	OPENFDA_API_URL="api.fda.gov"
	OPENFDA_API_EVENT="/drug/event.json"
	OPENFDA_API_DRUG='&search=patient.drug.medicinalproduct:'
	OPENFDA_API_COMPANY='&search='

	def get_event(self, limit):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL) #aqui se pone self porque la constante openfda_api_url esta definida dentro de la clase
		conn.request("GET", self.OPENFDA_API_EVENT + "?limit=" + limit)
		r1 = conn.getresponse()
		data1 = r1.read()
		data=data1.decode("utf8")
		biblioteca_data=json.loads(data)
		events=biblioteca_data
		return events

	def get_drug_search(self, drug_search):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		conn.request("GET", self.OPENFDA_API_EVENT +"?limit=10"+ self.OPENFDA_API_DRUG + drug_search)
		r1 = conn.getresponse()
		data1 = r1.read()
		data=data1.decode("utf8")
		biblioteca_data=json.loads(data)
		events_search=biblioteca_data
		return events_search

	def get_company_search(self, company_numb):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		conn.request("GET", self.OPENFDA_API_EVENT +"?limit=10"+ self.OPENFDA_API_COMPANY + company_numb)
		r1 = conn.getresponse()
		data1 = r1.read()
		data=data1.decode("utf8")
		biblioteca_data=json.loads(data)
		events_search=biblioteca_data
		return events_search

	def get_patient_sex(self, limit):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL) #aqui se pone self porque la constante openfda_api_url esta definida dentro de la clase
		conn.request("GET", self.OPENFDA_API_EVENT + "?limit=" + limit)
		r1 = conn.getresponse()
		data1 = r1.read()
		data=data1.decode("utf8")
		biblioteca_data=json.loads(data)
		events=biblioteca_data
		return events

class OpenFDAParser():
	def get_drugs(self, events):
		events=events["results"]
		medicamentos=[]
		for event in events:
			drug=event["patient"]["drug"][0]["medicinalproduct"]
			medicamentos += [drug]
		return medicamentos

	def get_companies_from_events(self, events):
		events=events["results"]
		companies=[]
		for event in events:
			companies+=[event['companynumb']]
		return companies

	def get_patientsex_from_events(self, events):
		events=events["results"]
		patientsex=[]
		for event in events:
			sex=event["patient"]["patientsex"]
			patientsex+=[sex]
		return patientsex

class OpenFDAHTML():
	def get_main_page(self):
		html= """
			<html>
				<head>
					<tittle>OpenFDA Cool App</tittle>
				</head>
				<body>
					<h1>OpenFDA Client</h1>
					<form method="get" action="listDrugs">
						<body>Number of events</body>
						<input type="text" size="3" name="limit">
						<input type="submit" value="Drug List: Enviar a OpenFDA">
					</form>
					<form method="get" action="searchDrug">
						<input type="submit" value="Drug Search LYRICA: Enviar to OpenFDA">
						<input type="text" name="drug"></input>
					</form>
					<form method="get" action="listCompanies">
						<body>Number of events</body>
						<input type="text" size="3" name="limit">
						<input type="submit" value="company list: Enviar a OpenFDA">
					</form>
					<form method="get" action="searchCompany">
						<input type="submit" value="Drug Search company: Enviar to OpenFDA">
						<input type="text" name="companynumb"></input>
					</form>
					<form method="get" action="listGender">
						<body>Number of events</body>
						<input type="text" size="3" name="limit">
						<input type="submit" value="Sex List: Enviar a OpenFDA">
					</form>
				</body>
			</html>
				"""
		return html

	def get_second_page(self, med):
		s=""
		for i in med:
			s += "<li>"+i+"</li>"
		html='''
		<html>
			<head></head>
				<body>
					<ol>
						%s
					</ol>
				</body>
		</html>''' %(s)
		return html

	def get_the_notfound_page(self):
		html="""
			<html>
				<head>
					<h1>Not found 404</h1>
				</head>
				<body>The host wasn't able to contact with the server</body>
			</html>
				"""
		return html


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	# GET
	def do_GET(self):

		client=OpenFDAClient()
		parser=OpenFDAParser()
		html_class=OpenFDAHTML()


		main_page=False
		is_event_drug=False
		is_event_company=False
		is_search_drug=False
		is_search_company=False
		is_patient_sex=False
		if self.path== '/':
			main_page=True
		elif 'listDrugs' in self.path:
			is_event_drug=True
		elif 'listCompanies' in self.path:
			is_event_company=True
		elif 'searchDrug' in self.path:
			is_search_drug=True
			print ('en slef.path search_drug')
		elif 'searchCompany' in self.path:
			is_search_company=True
		elif 'listGender' in self.path:
			is_patient_sex=True

		RESPONSE=200
		# Send response status code

		# Send headers



		if main_page:
			html=html_class.get_main_page()

		elif is_event_drug:
			limit=str(self.path.split('=')[1])
			if limit=='':
				limit='10'
			event=client.get_event(limit)
			drugs=parser.get_drugs(event)
			html=html_class.get_second_page(drugs)

		elif is_event_company:
			limit=str(self.path.split('=')[1])
			if limit=='':
				limit='10'
			event=client.get_event(limit)
			company=parser.get_companies_from_events(event)
			html=html_class.get_second_page(company)

		elif is_patient_sex:
			limit=str(self.path.split('=')[1])
			if limit=='':
				limit='10'
			event=client.get_patient_sex(limit)
			patient_sex=parser.get_patientsex_from_events(event)
			html=html_class.get_second_page(patient_sex)

		elif is_search_drug:
			drug=self.path.split('=')[1]
			event=client.get_drug_search(drug)
			companies=parser.get_companies_from_events(event)
			html=html_class.get_second_page(companies)

		elif is_search_company:
			company=self.path.split('=')[1]
			event=client.get_company_search(company)
			drugs=parser.get_drugs(event)
			html=html_class.get_second_page(drugs)

		else:
			RESPONSE=404
			html=html_class.get_the_notfound_page()

		self.send_response(RESPONSE)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(bytes(html, "utf8"))


		return
