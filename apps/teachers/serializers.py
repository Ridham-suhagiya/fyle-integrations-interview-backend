from attr import attr
from rest_framework import serializers
from apps.students.models import Assignment


class StudentAssignmentSerializer(serializers.ModelSerializer):
    """
    Student Assignment serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):
        

        
        if 'student' in attrs:
            raise serializers.ValidationError('Teacher cannot change the student who submitted the assignment')

        if 'state' in attrs:
            print('suhagiya')
            if attrs['state'] == 'GRADED':
                raise serializers.ValidationError('Student cannot set state to GRADED')
            if attrs['state'] == 'SUBMITTED' and not ('teacher' in attrs and attrs['teacher']):
                raise serializers.ValidationError('Teacher ID has to be sent to set state to SUBMITTED')
        if 'content' in attrs:
            raise serializers.ValidationError('Teacher cannot change the content of the assignment')
        
        # if attrs['user_id'] != attrs['teacher_id']:
        #     raise serializers.ValidationError('Teacher cannot grade for other teacher''s assignment')


        if self.partial:
            return attrs

        return super().validate(attrs)

    
