import requests
import time
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError

class RobustAPIClient:
    def __init__(self, base_url, timeout=10, max_retries=3):
        """
        Initialize API client with configuration

        Args:
            base_url: Base URL for API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    def _make_request(self, method, endpoint, **kwargs):
        """
        Make HTTP request with error handling and retries

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests

        Returns:
            Response object or None if failed
        """
        url = f"{self.base_url}/{endpoint}"

        for attempt in range(self.max_retries):
            try:
                # Make the request
                response = requests.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )

                # Check for HTTP errors
                response.raise_for_status()

                # Success!
                return response

            except Timeout:
                print(f"Timeout on attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                else:
                    print("Request timed out after all retries")
                    return None

            except ConnectionError:
                print(f"Connection error on attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    print("Cannot connect to server")
                    return None

            except HTTPError as e:
                # Don't retry on client errors (4xx)
                if 400 <= response.status_code < 500:
                    print(f"Client error: {response.status_code}")
                    return None

                # Retry on server errors (5xx)
                print(f"Server error on attempt {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    print("Server error persists")
                    return None

            except RequestException as e:
                print(f"Request failed: {e}")
                return None

        return None

    def get(self, endpoint, params=None):
        """Make GET request"""
        response = self._make_request('GET', endpoint, params=params)

        if response:
            try:
                return response.json()
            except ValueError:
                print("Invalid JSON in response")
                return None
        return None

    def post(self, endpoint, data=None):
        """Make POST request"""
        response = self._make_request('POST', endpoint, json=data)

        if response:
            try:
                return response.json()
            except ValueError:
                print("Invalid JSON in response")
                return None
        return None

# Example usage
def test_client():
    """Test the robust client"""

    # Create client for JSONPlaceholder
    client = RobustAPIClient("https://jsonplaceholder.typicode.com")

    # Test successful request
    print("Testing successful request:")
    posts = client.get("posts/1")
    if posts:
        print(f"Got post: {posts['title']}\n")

    # Test 404 error
    print("Testing 404 error:")
    result = client.get("posts/99999")
    if not result:
        print("Handled 404 correctly\n")

    # Test timeout (using a slow endpoint)
    print("Testing timeout handling:")
    slow_client = RobustAPIClient("https://httpbin.org", timeout=1)
    result = slow_client.get("delay/5")  # This endpoint delays 5 seconds

    # Test connection error (invalid domain)
    print("\nTesting connection error:")
    bad_client = RobustAPIClient("https://this-domain-does-not-exist-12345.com")
    result = bad_client.get("test")

if __name__ == "__main__":
    test_client()
