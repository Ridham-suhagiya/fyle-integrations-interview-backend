from django.shortcuts import render
from rest_framework import generics, status
from apps.students.models import Assignment
from .models import Teacher
from .serializers import StudentAssignmentSerializer
from rest_framework.response import Response

class AssignmentsView(generics.ListCreateAPIView):

	queryset = Teacher.objects.all()
	serializer_class = StudentAssignmentSerializer
	
	def get(self, request, *args, **kwargs):
	   
		
		assignments = Assignment.objects.filter(teacher__user=request.user)
		
		return Response(
			data= self.serializer_class(assignments, many=True).data,
			status=status.HTTP_200_OK,
		)


	def patch(self, request, *args, **kwargs):
		teacher = Teacher.objects.get(user=request.user)
		request.data['Teacher'] = teacher.id
		if 'student' in request.data:
			return Response(
				data= {'non_field_errors': ['Teacher cannot change the student who submitted the assignment']},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		

		if 'teacher_id' in request.data:
			
			teacher = Teacher.objects.get(pk=request.data['teacher_id'])
			request.data['teacher'] = teacher.id

		try:
			
			assignment = Assignment.objects.get(pk=request.data['id']	)
			assignment_data=Assignment.objects.filter(pk=request.data['id']).values()
			# if assignment.state != 'SUBMITTED':
			# 			serializer = self.serializer_class(assignment, data=request.data, partial=True)

		except Assignment.DoesNotExist:
			return Response(
				data={'error': 'Assignment does not exist/permission denied'},
				status=status.HTTP_400_BAD_REQUEST
			)

		serializer = self.serializer_class(assignment, data=request.data, partial=True)
		
		if serializer.is_valid():
			if assignment_data[0].get('teacher_id')!=request.user.id:
				print(assignment_data[0].get('teacher_id'),request.user.id)
				return Response(
					data={'non_field_errors':['Teacher cannot grade for other teacher''s assignment']},
					status=status.HTTP_400_BAD_REQUEST
					)
		
			if assignment.state == 'SUBMITTED':
					if assignment.grade is not None:
						assignment.state = 'GRADED'
						serializer.save()
						return Response(
							data=serializer.data,
							status=status.HTTP_200_OK
						)
					
				
		

			else:
				if assignment.state == 'GRADED':
					return Response(
								data={'non_field_errors':['GRADED assignments cannot be graded again']},
								status=status.HTTP_400_BAD_REQUEST
								)
				return Response(
					data={'non_field_errors':['SUBMITTED assignments can only be graded']},
					status=status.HTTP_400_BAD_REQUEST
					)
		

			
	

		return Response(
			data=serializer.errors,
			status=status.HTTP_400_BAD_REQUEST
		)