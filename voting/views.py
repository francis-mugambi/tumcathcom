from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import mainOfficeCadidate, choirCadidate, sccCadidate, cmaCadidate, claCadidate, voter
from .models import mainOfficePost, choirPost, cmaPost, claPost, sccPost, authenticateVoting
from portal.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.
def loginVoter(request):
    if request.method == "POST":       
        email = request.POST['email'].lower()
        password = request.POST['password']   

        check_email = User.objects.filter(email=email).exists()
        # check_voter = voter.objects.filter(name=email).exists()
        not_approved = User.objects.filter(email=email, is_approved=False).exists()
        authenticate_voting = authenticateVoting.objects.get(id=1)
        user = authenticate(request, username=email, password=password)
        
        if email =="" or password =="":
            return render(request, 'voting/login.html',{"msg1":"All the fields must be filled"})

        if check_email == False:
            return render(request, 'voting/login.html',{"msg1":"You are not a registered member!"})

        if user is  None:
            return render(request, 'voting/login.html',{"msg1":"Invalid Password!"})

        if not_approved :
            return render(request, 'voting/login.html',{"msg1":"You have not been approved for voting!"})

        if authenticate_voting.is_authenticated_voting == False:
            return render(request, 'voting/login.html',{"msg1":"Currently there is no Election!"})                     

        else:
            auth.login(request, user)			
            return redirect('vote-main-office')
            
    else:       
        return render(request, 'voting/login.html')

def logoutVoter(request, *args, **kwargs):
	auth.logout(request)
	return redirect('/')

###### MAIN OFFICE ELECTIONS #############################################################################
@login_required(login_url="login-voter")
def voteMainOffice(request): 
    cadidates = mainOfficeCadidate.objects.all()
    user_id = User.objects.get(email=request.user.email)
    check_voter = voter.objects.filter(name=user_id.id).exists()
    if check_voter == False:
        user_email = User.objects.get(email=request.user.email)
        add_voter = voter(name=user_email)
        add_voter.save()           

    context = {    
        'cadidates':cadidates,
    }       
    return render(request, 'voting/main_office.html', context)

@login_required(login_url="login-voter")
def addMainOfficeVote(request):
    if request.method == 'POST':
        cadidate_id = request.POST['vote']          
        user = User.objects.get(email=request.user.email)  
        voter_user = voter.objects.get(name=user)
        cadidate = mainOfficeCadidate.objects.get(id=cadidate_id)
        #posts
        # chairperson = mainOfficePost.objects.get(id=1)

        #1. Chairperson  
        if cadidate.post.id == 1: 
            if voter_user.voted_office_chairperson == True: 
                messages.info(request, f"You have aready casted for the {cadidate.post} post.")	          
                return redirect('vote-main-office')                     
            else:
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_office_chairperson = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-main-office')                
        #2.Vice Chairperson  
        elif cadidate.post.id == 2: 
            if voter_user.voted_vice_chairperson == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-main-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_vice_chairperson = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-main-office')          
        #3. secretary
        elif cadidate.post.id == 3: 
            if voter_user.voted_office_secretary == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-main-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_office_secretary = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-main-office')  
        
        #4. vice secretary
        elif cadidate.post.id == 4: 
            if voter_user.voted_vice_secretary == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-main-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_vice_secretary = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-main-office')  

        #5. Treasurer
        elif cadidate.post.id == 5: 
            if voter_user.voted_office_treasurer == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-main-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_office_treasurer = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-main-office')  
        
        #6. scc
        elif cadidate.post.id == 6: 
            if voter_user.voted_scc_leader == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-main-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_scc_leader = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-main-office')  

        #7. organizing secretary
        elif cadidate.post.id == 7: 
            if voter_user.voted_organizing_secretary == True:
                messages.info(request, f"You have aready casted for {cadidate.post}!")
                return redirect('vote-main-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_organizing_secretary = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-main-office')  

        #8. liturgical leader
        elif cadidate.post.id == 8: 
            if voter_user.voted_Liturgical_leader == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-main-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_Liturgical_leader = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-main-office')  

        #9. asset manager
        elif cadidate.post.id == 9: 
            if voter_user.voted_asset_manager == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-main-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_asst_Choir_director = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-main-office')  

        #10 .hospitality manager
        elif cadidate.post.id == 10: 
            if voter_user.voted_hospitality_manager == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-main-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_hospitality_manager = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-main-office')  
        
    return redirect('vote-main-office') 

###### CHOIR OFFICE ELECTIONS #############################################################################
@login_required(login_url="login-voter")
def voteChoirOffice(request): 
    cadidates = choirCadidate.objects.all()
    context = {        
        'cadidates':cadidates,     
    }          
    return render(request, 'voting/choir_office.html', context)

@login_required(login_url="login-voter")
def addChoirOfficeVote(request):
    if request.method == 'POST':
        cadidate_id = request.POST['vote']          
        user = User.objects.get(email=request.user.email)  
        voter_user = voter.objects.get(name=user)
        cadidate = choirCadidate.objects.get(id=cadidate_id)
        #posts
       
        #1. Chairperson  
        if cadidate.post.id == 1: 
            if voter_user.voted_choir_chairperson == True: 
                messages.info(request, f"You have aready casted for the {cadidate.post} post.")	          
                return redirect('vote-choir-office')                     
            else:
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_choir_chairperson = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-choir-office')                
        #2.Secretary  
        elif cadidate.post.id == 2: 
            if voter_user.voted_choir_secretary == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-choir-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_choir_secretary = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-choir-office')          
        #3. Treasurer
        elif cadidate.post.id == 3: 
            if voter_user.voted_choir_treasurer == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-choir-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_choir_treasurer = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-choir-office')  
        
        #4. Choir Director
        elif cadidate.post.id == 4: 
            if voter_user.voted_choir_director == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-choir-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_choir_director = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-choir-office')  

        #5. Assistant Choir Director
        elif cadidate.post.id == 5: 
            if voter_user.voted_asst_choir_director == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-choir-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_asst_choir_director = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-choir-office')  
        
        #6. Dancers Coordinator
        elif cadidate.post.id == 6: 
            if voter_user.voted_dancers_coordinator == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-choir-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_dancers_coordinator = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-choir-office')  

        #7. Dancers Secretary
        elif cadidate.post.id == 7: 
            if voter_user.voted_dancers_secretary == True:
                messages.info(request, f"You have aready casted for {cadidate.post}!")
                return redirect('vote-choir-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_dancers_secretary = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-choir-office')  

        #8. Praise and worship coordinator
        elif cadidate.post.id == 8: 
            if voter_user.voted_worship_coordinator == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-choir-office')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_worship_coordinator = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post} leader.")	          
                return redirect('vote-choir-office')  
        else:
            return redirect('vote-choir-office')
                        
    return redirect('vote-choir-office') 

###### CMA CLA OFFICE ELECTIONS #############################################################################
@login_required(login_url="login-voter")
def voteCmaClaOffice(request): 
    cma_cadidates = cmaCadidate.objects.all()
    cla_cadidates = claCadidate.objects.all()
    context = {        
        'cma_cadidates':cma_cadidates,          
        'cla_cadidates':cla_cadidates,    
    }             
    return render(request, 'voting/cma_cla_office.html', context)

@login_required(login_url="login-voter")
def addCmaLeadersVote(request):
    if request.method == 'POST':
        cadidate_id = request.POST['vote']          
        user = User.objects.get(email=request.user.email)  
        voter_user = voter.objects.get(name=user)
        cma_cadidate = cmaCadidate.objects.get(id=cadidate_id)
        #posts
        cma_chairperson = cmaPost.objects.get(id=1)
        cma_secretary = cmaPost.objects.get(id=2)
        #1. CMA Chairperson  
        if cma_cadidate.post.id == 1: 
            if voter_user.voted_cma_chairperson == True: 
                messages.info(request, f"You have aready casted for the {cadidate.post} post.")	          
                return redirect('vote-cma-cla-office')                     
            else:
                cma_cadidate.votes = cma_cadidate.votes + 1
                cma_cadidate.save() 
                voter_user.voted_cma_chairperson = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-cma-cla-office')                
        #2. CMA Secretary  
        elif cma_cadidate.post.id == 2: 
            if voter_user.voted_cma_secretary == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-cma-cla-office')           
            else : 
                cma_cadidate.votes = cma_cadidate.votes + 1
                cma_cadidate.save() 
                voter_user.voted_cma_secretary = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-cma-cla-office')                
    return redirect('vote-cma-cla-office') 

@login_required(login_url="login-voter")
def addClaLeadersVote(request):
    if request.method == 'POST':
        cadidate_id = request.POST['vote']          
        user = User.objects.get(email=request.user.email)  
        voter_user = voter.objects.get(name=user)
        cla_cadidate = claCadidate.objects.get(id=cadidate_id)
        #posts
        cla_chairperson = claPost.objects.get(id=1)
        cla_secretary = claPost.objects.get(id=2)
        #1. CLA Chairperson  
        if cla_cadidate.post.id == 1: 
            if voter_user.voted_cla_chairperson == True: 
                messages.info(request, f"You have aready casted for the {cadidate.post} post.")	          
                return redirect('vote-cma-cla-office')                     
            else:
                cla_cadidate.votes = cla_cadidate.votes + 1
                cla_cadidate.save() 
                voter_user.voted_cla_chairperson = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-cma-cla-office')                
        #2. CLA Secretary  
        elif cla_cadidate.post.id == 2: 
            if voter_user.voted_cla_secretary == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-cma-cla-office')           
            else : 
                cla_cadidate.votes = cla_cadidate.votes + 1
                cla_cadidate.save() 
                voter_user.voted_cla_secretary = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-cma-cla-office')  
    return redirect('vote-cma-cla-office') 

###### SCC OFFICE ELECTIONS #############################################################################
@login_required(login_url="login-voter")
def voteSccLeaders(request): 
    cadidates = sccCadidate.objects.all() 
    context = {        
        'cadidates':cadidates,     
    }               
    return render(request, 'voting/scc_leaders.html',context)

@login_required(login_url="login-voter")
def addSccLeadersVote(request):
    if request.method == 'POST':
        cadidate_id = request.POST['vote']          
        user = User.objects.get(email=request.user.email)  
        voter_user = voter.objects.get(name=user)
        cadidate = sccCadidate.objects.get(id=cadidate_id)

        #1. Chairperson  
        if cadidate.post.id == 1: 
            if voter_user.voted_family_chairperson == True: 
                messages.info(request, f"You have aready casted for the {cadidate.post} post.")	          
                return redirect('vote-scc-leaders')                     
            else:
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_family_chairperson = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-scc-leaders')                
        #2.Secretary  
        elif cadidate.post.id == 2: 
            if voter_user.voted_family_secretary == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-scc-leaders')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_family_secretary = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-scc-leaders')          
        #3. Project Manager
        elif cadidate.post.id == 3: 
            if voter_user.voted_project_manager == True:
                messages.info(request, f"You have aready casted for {cadidate.post} post!")
                return redirect('vote-scc-leaders')           
            else : 
                cadidate.votes = cadidate.votes + 1
                cadidate.save() 
                voter_user.voted_project_manager = True 
                voter_user.save()
                messages.info(request, f"Vote casted for {cadidate.post}.")	          
                return redirect('vote-scc-leaders')  
       
    return redirect('vote-scc-leaders') 
###### ELECTIONS RESULTS #############################################################################
@login_required(login_url="login-voter")
def results(request): 
    main_office_results = mainOfficeCadidate.objects.all().order_by('post','-votes')
    choir_office_results = choirCadidate.objects.all().order_by('post','-votes')
    context = {
        'main_office_results':main_office_results,
        'choir_office_results':choir_office_results,
    }   
    return render(request, 'voting/results.html', context)

