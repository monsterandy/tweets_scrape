import io
from google.cloud import vision

# def detect_text(path):
#     """Detects text in the file."""
#     from google.cloud import vision
#     import io
#     client = vision.ImageAnnotatorClient()

#     with io.open(path, 'rb') as image_file:
#         content = image_file.read()

#     image = vision.Image(content=content)

#     response = client.text_detection(image=image, image_context={"language_hints": ["en"]},)
#     text = response.full_text_annotation.text
#     text = text.replace('\n', ' ')

#     if response.error.message:
#         raise Exception(
#             '{}\nFor more info on error messages, check: '
#             'https://cloud.google.com/apis/design/errors'.format(
#                 response.error.message))
#     return text


class GoogleVision:
    def __init__(self) -> None:
        self.client = vision.ImageAnnotatorClient()

    def detect_text_label_safesearch(self, path):
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        
        response = self.client.annotate_image({
            'image': {'content': image.content},
            'features': [{'type_': vision.Feature.Type.TEXT_DETECTION},
                        {'type_': vision.Feature.Type.LABEL_DETECTION, 'max_results': 5},
                        {'type_': vision.Feature.Type.SAFE_SEARCH_DETECTION}],
            'image_context': {'language_hints': ['en']}
        })

        text = response.full_text_annotation.text
        text = text.replace('\n', ' ')

        labels = []
        for label in response.label_annotations:
            if label.score > 0.5:
                labels.append(label.description)
            
        lb = ','.join(labels)

        safe = response.safe_search_annotation
        safe_search = []

        if safe.adult >= 3:
            safe_search.append('adult')

        if safe.spoof >= 3:
            safe_search.append('spoof')

        if safe.medical >= 3:
            safe_search.append('medical')

        if safe.violence >= 3:
            safe_search.append('violence')

        if safe.racy >= 3:
            safe_search.append('racy')

        explicit = ','.join(safe_search)

        return text, lb, explicit

    def detect_label_safesearch(self, path):
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        
        response = self.client.annotate_image({
            'image': {'content': image.content},
            'features': [{'type_': vision.Feature.Type.LABEL_DETECTION, 'max_results': 5},
                        {'type_': vision.Feature.Type.SAFE_SEARCH_DETECTION}]
        })

        labels = []
        for label in response.label_annotations:
            if label.score > 0.5:
                labels.append(label.description)
            
        lb = ','.join(labels)

        safe = response.safe_search_annotation
        safe_search = []

        if safe.adult >= 3:
            safe_search.append('adult')

        if safe.spoof >= 3:
            safe_search.append('spoof')

        if safe.medical >= 3:
            safe_search.append('medical')

        if safe.violence >= 3:
            safe_search.append('violence')

        if safe.racy >= 3:
            safe_search.append('racy')

        explicit = ','.join(safe_search)

        return lb, explicit
