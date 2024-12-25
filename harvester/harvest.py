import logging
import requests
import time

class Harvest:

    def __init__(self, config):
        self.config = config
        self.wait_time = float(config.get('WaitTime', 1.0))  # Default wait time to 1.0 seconds if not provided
        self.logger = logging.getLogger(__name__)


    def reviews(self, property_id):
        """
        Iterate through review pages and collects them.

        This method is responsible for gathering reviews,
        cleaning the data, and storing it in a structured format for further analysis.

        Steps:
            Access ReviewsUrl
                With property_id being the ID of the property.
            Get the json response and save the elements of "reviews" in a collection
            Navigate to pagination.next until null and repeat above steps
            Return the collection

        Returns:
            list: A list of processed reviews.
        """
        review_url = self.config['BaseUrl'] + self.config['ReviewsUrl']
        page = 1
        review_list = []

        while True:
            time.sleep(self.wait_time)  # Wait between requests
            url = review_url.format(property_id, page)
            response = requests.get(url)
            if response.status_code != 200:
                self.logger.error(
                    "Failed to fetch reviews. " +
                    "Property: '%s'. " +
                    "Url: '%s'. "+
                    "Status Code: '%s'. "
                    , property_id, url, response.status_code)
                break

            data = response.json()
            review_list.extend(data.get("reviews", []))

            if not data.get("pagination", {}).get("next"):
                break

            page += 1

        return review_list


    def property(self, property_id):
        """
        Collects property details.

        This method is responsible for gathering property details,
        cleaning the data, and storing it in a structured format for further analysis.

        Steps:
            Access PropertyUrl
                With property_id being the ID of the property.
            Get all property fields except for:
                - reviews
                - images
                - imagesGallery
            Start Harvest.reviews with same id

        Returns:
            list: Property id.
        """
        property_url = self.config['BaseUrl'] + self.config['PropertyUrl'].format(property_id)

        response = requests.get(property_url)
        if response.status_code != 200:
            self.logger.error(
                "Failed to fetch property details. " +
                "Property: '%s'. " +
                "Url: '%s'. " +
                "Status Code: '%s'. "
                , property_id, property_url, response.status_code)
            return None

        data = response.json()
        # Remove unwanted fields
        data.pop("reviews", None)
        data.pop("images", None)
        data.pop("imagesGallery", None)

        # Start review_harvester with the same property_id
        review_list = self.reviews(property_id)
        data["reviews"] = review_list

        self.logger.info("Finished harvesting property '%s'. ", property_id)

        return data