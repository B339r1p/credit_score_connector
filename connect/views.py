from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from connect.serializers import EligibilitySerializers
from get_score import get_score_and_eligibility


class EligibilityChecksAPIView(APIView):
    def post(self, request, format=None):
        serializer = EligibilitySerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]

        score_and_eligibility = get_score_and_eligibility(phone_number)
        eligible = score_and_eligibility.get("eligible")

        if eligible is True:
            return Response(score_and_eligibility, status=status.HTTP_200_OK)
        else:
            return Response(score_and_eligibility, status=status.HTTP_400_BAD_REQUEST)


# class QueryTanadiDatabaseAPIView(APIView):
#     def get(self, request, format=None):
#         phone_number = request.query_params.post("phone_number")
