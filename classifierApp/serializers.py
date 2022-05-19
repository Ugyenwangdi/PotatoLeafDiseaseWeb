from rest_framework import serializers

from .models import Result, APIResult

### option 2...Also this can be done with view 1 but this time it is using model serializer...keeping code more concise
class LeafDiseaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result
        fields = ('id', 'imagelink', 'predicted', 'confidence', 'saved')

class APILeafDiseaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = APIResult
        fields = ('id', 'imagename', 'imagelink', 'predicted', 'confidence', 'saved')
