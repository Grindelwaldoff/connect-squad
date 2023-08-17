from rest_framework import serializers

class ZipFileSerializer(serializers.Serializer):
    session_file = serializers.FileField()
