from django.shortcuts import render, redirect
from .forms import UserInfoForm, AnswersForm
from .utils import generate_scenario, analyze_texts, scores_from_sentiments
from .models import Submission
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .eq_engine import EQEngine

def landing(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            # store in session and redirect
            request.session['age'] = form.cleaned_data['age']
            request.session['gender'] = form.cleaned_data['gender']
            request.session['profession'] = form.cleaned_data['profession']
            return redirect('assessment:scenario')
    else:
        form = UserInfoForm()
    return render(request, 'assessment/landing.html', {'form': form})

def scenario_view(request):
    age = request.session.get('age')
    profession = request.session.get('profession')
    scenario = generate_scenario(profession, age)
    
    if request.method == 'POST':
        form = AnswersForm(request.POST)
        if form.is_valid():
            answers = {
                'q1': form.cleaned_data['answer_1'],
                'q2': form.cleaned_data['answer_2'],
                'q3': form.cleaned_data['answer_3'],
            }
            
            # Show loading message
            request.session['processing'] = True
            request.session.save()
            
            try:
                # Analyze responses
                texts = list(answers.values())
                analysis_results = analyze_texts(texts)  # Use optimized version
                
                
                engine = EQEngine()
                scores = engine.compute(list(answers.values()))
                
                sub = Submission.objects.create(
                    age=age,
                    gender=request.session.get('gender', ''),
                    profession=profession,
                    scenario=scenario,
                    answers=answers,
                    scores=scores,
                )
                request.session['last_submission_id'] = sub.id
                request.session['processing'] = False
                return redirect('assessment:results')
                
            except Exception as e:
                # Fallback to simple scoring if analysis fails
                scores = {'overall': 50, 'self_awareness': 50, 'emotional_regulation': 50, 
                         'empathy': 50, 'conflict_resolution': 50, 'motivation': 50, 'social_skills': 50}
                # ... create submission with fallback scores
                return redirect('assessment:results')
    else:
        form = AnswersForm()
    
    return render(request, 'assessment/scenario.html', {'scenario': scenario, 'form': form})

import json

def get_eq_feedback(overall_score):
    """
    Determine EQ level and provide feedback based on overall score
    """
    if overall_score >= 80:
        level = "High EQ"
        feedback = "Excellent! You demonstrate strong emotional intelligence with advanced self-awareness, empathy, and relationship management skills. You're likely effective at navigating complex social situations and managing emotions constructively."
        color = "#28a745"  # Green
    elif overall_score >= 60:
        level = "Above Average EQ"
        feedback = "Good emotional intelligence! You have solid foundational skills with room for growth in specific areas. You generally handle emotions well but may benefit from further developing certain EQ competencies."
        color = "#17a2b8"  # Blue
    elif overall_score >= 40:
        level = "Average EQ"
        feedback = "You have basic emotional awareness with opportunities for significant development. Focus on improving self-reflection, empathy, and emotional regulation to enhance your interpersonal effectiveness."
        color = "#ffc107"  # Yellow
    elif overall_score >= 20:
        level = "Below Average EQ"
        feedback = "There's considerable room for growth in emotional intelligence. Consider developing fundamental skills in emotional awareness, self-regulation, and social awareness through practice and learning."
        color = "#fd7e14"  # Orange
    else:
        level = "Low EQ"
        feedback = "Emotional intelligence development should be a priority. Focus on building basic self-awareness and understanding emotions in yourself and others. Consider seeking resources or training in emotional intelligence fundamentals."
        color = "#dc3545"  # Red
    
    return {
        'level': level,
        'feedback': feedback,
        'color': color
    }

def results_view(request):
    sub_id = request.session.get('last_submission_id')
    if not sub_id:
        return redirect('assessment:landing')
    
    try:
        sub = Submission.objects.get(pk=sub_id)
    except Submission.DoesNotExist:
        return redirect('assessment:landing')
    
    overall_score = sub.scores.get('overall', 0)
    eq_feedback = get_eq_feedback(overall_score)
    categories = {k: v for k, v in sub.scores.items() if k != 'overall'}
    labels = list(categories.keys())
    data = list(categories.values())
    
    return render(request, 'assessment/results.html', {
        'submission': sub,
        'categories': categories,
        'overall': overall_score,
        'eq_feedback': eq_feedback,
        'labels_json': json.dumps(labels),
        'data_json': json.dumps(data),
    })