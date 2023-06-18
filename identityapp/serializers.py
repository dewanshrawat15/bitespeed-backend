from rest_framework import serializers
from .models import Contact


class ContactRequestSerializer(serializers.ModelSerializer):

    def is_valid(self, *, raise_exception=False):
        has_errors = False
        super(ContactRequestSerializer, self).is_valid()
        data = dict(self.validated_data)
        if len(data.keys()) == 0:
            has_errors = True
        else:
            phoneNumber = data.get('phoneNumber', None)
            email = data.get('email', None)
            if phoneNumber is None and email is None:
                has_errors = True
        return not has_errors

    class Meta:
        model = Contact
        fields = ('phoneNumber', 'email')
