from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .serializers import ContactRequestSerializer
from .models import Contact

# Create your views here.


def check_if_records_dont_exist(data) -> bool:
    return len(data) == 0


def get_response(email, phoneNumber):
    records = Contact.objects.filter(email=email) | Contact.objects.filter(phoneNumber=phoneNumber)
    if check_if_records_dont_exist(records):
        return {
            "contact": {
                "primaryContactId": "",
                "emails": [],
                "phoneNumbers": [],
                "secondaryContactIds": []
            }
        }
    else:
        primaryContact = records.filter(linkPrecedence=1)[0]
        secondaryContacts = records.filter(linkPrecedence=2)
        return {
            "contact": {
                "primaryContactId": primaryContact.id,
                "emails": list(set([primaryContact.email] + [contact.email for contact in secondaryContacts])),
                "phoneNumbers": list(set([primaryContact.phoneNumber] + [contact.phoneNumber for contact in secondaryContacts])),
                "secondaryContactIds": list(set(contact.id for contact in secondaryContacts))
            }
        }


class IdentityView(APIView):
    serializer_class = ContactRequestSerializer

    def post(self, request):
        serializer = ContactRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = dict(serializer.validated_data)
            email = data.get('email', None)
            phoneNumber = data.get('phoneNumber', None)

            records_against_email = Contact.objects.filter(email=email if email is not None else -1)
            records_against_phone_number = Contact.objects.filter(phoneNumber=phoneNumber if phoneNumber is not None else -1)

            if check_if_records_dont_exist(records_against_email) and check_if_records_dont_exist(records_against_phone_number):
                Contact.objects.create(
                    phoneNumber=phoneNumber,
                    email=email,
                    id=len(Contact.objects.all()) + 1,
                    createdAt=timezone.now(),
                    updatedAt=timezone.now()
                ).save()
            else:
                # elements in A and elements in B
                primary_common_records = (records_against_email | records_against_phone_number).filter(linkPrecedence=1)
                if len(primary_common_records) > 1:
                    primaryContactAgainstEmail = records_against_email.filter(linkPrecedence=1)[0]
                    primaryContactAgainstNumber = records_against_phone_number.filter(linkPrecedence=1)[0]

                    primaryContactAgainstNumber.linkedId = primaryContactAgainstEmail.id
                    primaryContactAgainstNumber.linkPrecedence = 2
                    primaryContactAgainstNumber.save()
                else:
                    primaryContact = (records_against_email | records_against_phone_number).filter(linkPrecedence=1)[0]
                    Contact.objects.create(
                        phoneNumber=phoneNumber,
                        email=email,
                        id=len(Contact.objects.all()) + 1,
                        createdAt=timezone.now(),
                        updatedAt=timezone.now(),
                        linkedId=primaryContact.id,
                        linkPrecedence=2
                    ).save()
            response = get_response(email, phoneNumber)
            return Response(response, status=status.HTTP_200_OK)

        return Response({
            "message": "Request not valid"
        }, status=status.HTTP_400_BAD_REQUEST)
