#!/usr/bin/env python
import requests
from google.protobuf.json_format import MessageToJson
from google.transit import gtfs_realtime_pb2

def fetch_gtfs_data(url):
    """
    Fetches GTFS realtime data from the given URL.
    
    :param url: URL of the GTFS realtime feed.
    :return: Binary content from the response.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request failed
    return response.content

def parse_gtfs_data(binary_data):
    """
    Parses the binary GTFS realtime data using the Protocol Buffers definition.
    
    :param binary_data: Binary data from the GTFS realtime feed.
    :return: Parsed FeedMessage object.
    """
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(binary_data)
    return feed

def main():
    # URL for the MTA GTFS realtime feed for J/Z trains
    url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz"
    
    try:
        binary_data = fetch_gtfs_data(url)
        feed = parse_gtfs_data(binary_data)
        
        # Convert the protobuf object to JSON
        json_feed = MessageToJson(feed)
        
        # Print the JSON output to the terminal
        print(json_feed)
        
        # Save the JSON output to a text file
        with open("gtfs_output.json", "w") as f:
            f.write(json_feed)
        print("GTFS JSON data has been saved to gtfs_output.json")
    
    except requests.RequestException as e:
        print("Error fetching GTFS data:", e)
    except Exception as e:
        print("An error occurred while processing the feed:", e)

if __name__ == "__main__":
    main()
