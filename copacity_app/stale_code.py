# @login_required
# def checkIns(request, nameId):
#     """The page to view all checkIns."""
#     resultSet = []
#     print("name:")
#     print(nameId)
#     print("user:")
#     print(request.user)
#     count = 0
# #    resultSet = CircleMembership.objects.filter(user=1)
# #    resultSet = CheckIn.objects.filter(owner=3)
#     resultSet = Circle.objects.all()
#     for result in resultSet:
#         count = count + 1
#         print("members: ")
#         print(type(result.members))
#         print("Circle")
#         print(result.name)
#     print("count: " + str(count))
#     if nameId == 0:
#         if request.user.id == 1:
#             results = CheckIn.objects.order_by('-dateTime')
#         else:
#             results = CheckIn.objects.filter(owner=request.user).order_by('-dateTime')
#     else:
#         if request.user.username == 'mcnalj':
#             results = CheckIn.objects.filter(yourName=nameId).order_by('-dateTime')
#         else:
#             results = CheckIn.objects.filter(owner=request.user).order_by('-dateTime')
#     top = len(results)
#     if top > 5:
#         top = 5
#
#     checkIns = []
#     count = 0
#     for result in results:
#         count = count + 1
#         if count <= top:
#             checkIn = {}
#             yourName = ""
#             safeThoughts = 0
#             safeActions = 0
#             urgency = 4
#
#             if result.yourName == 1:
#                 yourName = "Jake"
#             elif result.yourName == 2:
#                 yourName = "Leah"
#             elif result.yourName == 3:
#                 yourName = "Raizel"
#             elif result.yourName == 4:
#                 yourName = "Oscar"
#
#             if result.thoughts == 1:
#                 safeThoughts = "Yes"
#             elif result.thoughts == 2:
#                 safeThoughts = "No"
#             elif result.thoughts == 3:
#                 safeThoughts = "Maybe"
#
#             if result.actions == 1:
#                 safeActions = "Yes"
#             elif result.actions == 2:
#                 safeActions = "No"
#             elif result.actions == 3:
#                 safeActions = "Maybe"
#
#             if result.urgency == 1:
#                 urgency = "Call now"
#             elif result.urgency == 2:
#                 urgency = "Text now"
#             elif result.urgency == 3:
#                 urgency = "We can talk later"
#             elif result.urgency == 4:
#                 urgency = "Not necessary to talk about it"
#             elif result.urgency == 5:
#                 urgency = "I prefer not to talk about it"
#             checkIn = {
#                         'id': result.id,
#                         'dateTime': result.dateTime,
#                         'yourName': yourName,
#                         'hardToday': result.hardToday,
#                         'goodToday': result.goodToday,
#                         'excitedToday': result.excitedToday,
#                         'thoughts': safeThoughts,
#                         'thoughtsExplained': result.thoughtsExplained,
#                         'actions': safeActions,
#                         'actionsExplained': result.actionsExplained,
#                         'moodRange': result.moodRange,
#                         'pintaRange': result.pintaRange,
#                         'urgency': urgency
#                         }
#             checkIns.append(checkIn)
#
#     context = {'checkIns': checkIns}
#     return render(request, 'copacity_app/checkIns.html', context)
# from yourCheckIns
    # results = CircleMembership.objects.filter(user=request.user)
    # circles = []
    # for result in results:
    #     print(result.circle.id)
    #     circle = {
    #         'circleId': result.circle.id,
    #         'name': result.circle.name,
    #         'poeple': result.circle.members.all()
    #     }
    #     circles.append(circle)
