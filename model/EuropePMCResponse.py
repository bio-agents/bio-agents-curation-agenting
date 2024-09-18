class EuropePMCResponse:
    def __init__(self, response_data):
        """
        Initializes the EuropePMCResponse object with data from a Europe PMC search query response.
        
        :param response_data: The JSON response data from a Europe PMC search query.
        """
        self.version = response_data.get('version')
        self.hit_count = response_data.get('hitCount')
        self.request = response_data.get('request', {})
        self.results = response_data.get('resultList', {}).get('result', [])
        
        # Extracting detailed attributes from the first result, if available
        first_result = self.results[0] if self.results else {}
        self.id = first_result.get('id')
        self.source = first_result.get('source')
        self.doi = first_result.get('doi')
        self.title = first_result.get('title')
        # self.author_string = first_result.get('authorString')
        self.authors = first_result.get('authorList', {}).get('author', [])
        self.publication_year = first_result.get('pubYear')
        self.abstract_text = first_result.get('abstractText')
        self.pub_types = first_result.get('pubTypeList', {}).get('pubType', [])
        # self.publisher = first_result.get('bookOrReportDetails', {}).get('publisher')
        self.year_of_publication = first_result.get('bookOrReportDetails', {}).get('yearOfPublication')
        self.full_text_urls = first_result.get('fullTextUrlList', {}).get('fullTextUrl', [])
        self.date_of_creation = first_result.get('dateOfCreation')
        self.first_index_date = first_result.get('firstIndexDate')
        self.first_publication_date = first_result.get('firstPublicationDate')

    def get_version(self):
        """Returns the version of the response."""
        return self.data.get('version')

    def get_hit_count(self):
        """Returns the total number of hits/result count."""
        return self.data.get('hitCount')

    def get_query_details(self):
        """Returns details of the request/query."""
        return self.data.get('request', {})

    def get_results(self):
        """Returns a list of result items."""
        return self.data.get('resultList', {}).get('result', [])

    def get_first_result(self):
        """Returns the first result item, if available."""
        results = self.get_results()
        return results[0] if results else None

    # def extract_publication_info(self):
    #     """
    #     Extracts and returns publication information from the first result.
        
    #     :return: A dictionary containing publication info such as title, doi, authors, abstract, and publication year.
    #     """
    #     result = self.get_first_result()
    #     if not result:
    #         return {}

    #     publication_info = {
    #         'title': result.get('title'),
    #         'doi': result.get('doi'),
    #         'authors': result.get('authorString'),
    #         'abstract': result.get('abstractText'),
    #         'publication_year': result.get('pubYear'),
    #         'full_text_url': [url.get('url') for url in result.get('fullTextUrlList', {}).get('fullTextUrl', []) if url.get('site') == 'DOI']
    #     }

    #     return publication_info
