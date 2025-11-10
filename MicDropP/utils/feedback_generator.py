"""
Generate feedback and recommendations based on analysis results
"""

def generate_voice_feedback(voice_metrics):
    """
    Generate feedback for voice analysis
    
    Args:
        voice_metrics: Dictionary with voice analysis metrics
    
    Returns:
        feedback: Dictionary with scores and recommendations
    """
    feedback = {
        'scores': {},
        'recommendations': []
    }
    
    # Pace feedback (optimal: 140-160 WPM)
    wpm = voice_metrics.get('pace', {}).get('wpm', 0)
    if wpm < 120:
        feedback['scores']['pace'] = 'slow'
        feedback['recommendations'].append(
            f"Your speaking pace is {wpm:.0f} WPM, which is slower than ideal (140-160 WPM). "
            "Try to speak a bit faster to maintain audience engagement."
        )
    elif wpm > 180:
        feedback['scores']['pace'] = 'fast'
        feedback['recommendations'].append(
            f"Your speaking pace is {wpm:.0f} WPM, which is quite fast. "
            "Consider slowing down slightly to ensure clarity and allow your audience to process information."
        )
    else:
        feedback['scores']['pace'] = 'good'
        feedback['recommendations'].append(
            f"Great! Your speaking pace of {wpm:.0f} WPM is within the ideal range."
        )
    
    # Pause feedback
    pause_count = voice_metrics.get('pauses', {}).get('count', 0)
    avg_pause_duration = voice_metrics.get('pauses', {}).get('avg_duration', 0)
    
    if pause_count < 3:
        feedback['scores']['pauses'] = 'few'
        feedback['recommendations'].append(
            "You have very few pauses. Strategic pauses help emphasize key points and give your audience time to process information."
        )
    elif pause_count > 15:
        feedback['scores']['pauses'] = 'many'
        feedback['recommendations'].append(
            f"You have {pause_count} pauses, which may be too many. Consider reducing unnecessary pauses for better flow."
        )
    else:
        feedback['scores']['pauses'] = 'good'
        feedback['recommendations'].append(
            f"Good use of pauses ({pause_count} pauses). This helps with clarity and emphasis."
        )
    
    # Pitch feedback
    monotony_score = voice_metrics.get('pitch', {}).get('monotony_score', 0.5)
    if monotony_score > 0.7:
        feedback['scores']['pitch'] = 'monotone'
        feedback['recommendations'].append(
            "Your voice shows limited pitch variation. Try varying your pitch more to add energy and engagement to your speech."
        )
    elif monotony_score < 0.3:
        feedback['scores']['pitch'] = 'varied'
        feedback['recommendations'].append(
            "Excellent pitch variation! Your voice is expressive and engaging."
        )
    else:
        feedback['scores']['pitch'] = 'good'
        feedback['recommendations'].append(
            "Good pitch variation. Your voice maintains interest without being overly dramatic."
        )
    
    # Volume feedback
    volume_consistency = voice_metrics.get('volume', {}).get('volume_consistency', 0.5)
    if volume_consistency < 0.5:
        feedback['scores']['volume'] = 'inconsistent'
        feedback['recommendations'].append(
            "Your volume varies significantly. Try to maintain a more consistent volume level for better clarity."
        )
    else:
        feedback['scores']['volume'] = 'consistent'
        feedback['recommendations'].append(
            "Good volume consistency. Your voice maintains steady volume throughout."
        )
    
    return feedback


def generate_language_feedback(language_metrics):
    """
    Generate feedback for language analysis
    
    Args:
        language_metrics: Dictionary with language analysis metrics
    
    Returns:
        feedback: Dictionary with scores and recommendations
    """
    feedback = {
        'scores': {},
        'recommendations': []
    }
    
    # Filler words feedback
    filler_stats = language_metrics.get('filler_words', {})
    filler_count = filler_stats.get('filler_count', 0)
    filler_rate = filler_stats.get('filler_rate', 0.0)
    total_words = filler_stats.get('total_words', 0)
    
    if filler_rate > 3.0:  # More than 3 fillers per 100 words
        feedback['scores']['filler_words'] = 'high'
        feedback['recommendations'].append(
            f"You used {filler_count} filler words ({filler_rate:.1f} per 100 words). "
            "Try to reduce filler words like 'um', 'uh', and 'like' to sound more confident and professional."
        )
    elif filler_rate > 1.5:
        feedback['scores']['filler_words'] = 'moderate'
        feedback['recommendations'].append(
            f"You used {filler_count} filler words. While acceptable, reducing them further will improve your delivery."
        )
    else:
        feedback['scores']['filler_words'] = 'low'
        feedback['recommendations'].append(
            f"Excellent! You used only {filler_count} filler words. Your speech is clear and confident."
        )
    
    # Vocabulary diversity feedback
    vocab_stats = language_metrics.get('vocabulary', {})
    diversity_ratio = vocab_stats.get('diversity_ratio', 0.0)
    
    if diversity_ratio < 0.4:
        feedback['scores']['vocabulary'] = 'low'
        feedback['recommendations'].append(
            f"Your vocabulary diversity is {diversity_ratio*100:.1f}%. "
            "Consider using more varied word choices to make your speech more engaging."
        )
    elif diversity_ratio > 0.7:
        feedback['scores']['vocabulary'] = 'high'
        feedback['recommendations'].append(
            f"Great vocabulary diversity ({diversity_ratio*100:.1f}%)! Your word choice is varied and engaging."
        )
    else:
        feedback['scores']['vocabulary'] = 'good'
        feedback['recommendations'].append(
            f"Good vocabulary diversity ({diversity_ratio*100:.1f}%). Your word choice is appropriate."
        )
    
    # Readability feedback
    readability = language_metrics.get('readability', {})
    flesch_score = readability.get('flesch_reading_ease', 0)
    
    if flesch_score > 0:
        if flesch_score < 30:
            feedback['scores']['readability'] = 'difficult'
            feedback['recommendations'].append(
                f"Your speech has a Flesch Reading Ease score of {flesch_score:.0f}, indicating it may be difficult to follow. "
                "Consider simplifying sentence structure and using shorter sentences."
            )
        elif flesch_score > 70:
            feedback['scores']['readability'] = 'easy'
            feedback['recommendations'].append(
                f"Your speech has a Flesch Reading Ease score of {flesch_score:.0f}, making it easy to understand. Great job!"
            )
        else:
            feedback['scores']['readability'] = 'moderate'
            feedback['recommendations'].append(
                f"Your speech has a Flesch Reading Ease score of {flesch_score:.0f}, which is appropriate for most audiences."
            )
    
    # Sentence structure feedback
    sentence_stats = language_metrics.get('sentence_structure', {})
    avg_words_per_sentence = sentence_stats.get('avg_words_per_sentence', 0)
    long_sentences = sentence_stats.get('long_sentences_count', 0)
    
    if avg_words_per_sentence > 20:
        feedback['scores']['sentence_structure'] = 'complex'
        feedback['recommendations'].append(
            f"Your average sentence length is {avg_words_per_sentence:.1f} words, which may be too long. "
            "Consider breaking complex sentences into shorter, clearer ones."
        )
    elif avg_words_per_sentence < 10:
        feedback['scores']['sentence_structure'] = 'simple'
        feedback['recommendations'].append(
            f"Your sentences are quite short (average {avg_words_per_sentence:.1f} words). "
            "While clear, varying sentence length can add rhythm and interest to your speech."
        )
    else:
        feedback['scores']['sentence_structure'] = 'good'
        feedback['recommendations'].append(
            f"Good sentence structure! Your average sentence length ({avg_words_per_sentence:.1f} words) is appropriate."
        )
    
    if long_sentences > 0:
        feedback['recommendations'].append(
            f"You have {long_sentences} sentence(s) with more than 25 words. Consider simplifying these for better clarity."
        )
    
    # Repetition feedback
    repetition_stats = language_metrics.get('repetition', {})
    repetition_score = repetition_stats.get('repetition_score', 0.0)
    most_repeated = repetition_stats.get('most_repeated', [])
    
    if repetition_score > 15:
        feedback['scores']['repetition'] = 'high'
        if most_repeated:
            top_words = ', '.join([f"'{word}' ({count}x)" for word, count in most_repeated[:3]])
            feedback['recommendations'].append(
                f"You have significant word repetition ({repetition_score:.1f}%). "
                f"Most repeated words: {top_words}. Consider using synonyms to add variety."
            )
    elif repetition_score > 8:
        feedback['scores']['repetition'] = 'moderate'
        feedback['recommendations'].append(
            f"Some word repetition detected ({repetition_score:.1f}%). Consider varying your word choice slightly."
        )
    else:
        feedback['scores']['repetition'] = 'low'
        feedback['recommendations'].append(
            "Good! Minimal word repetition detected. Your language is varied and engaging."
        )
    
    # Tone feedback
    tone_stats = language_metrics.get('tone', {})
    engagement_score = tone_stats.get('engagement_score', 0.0)
    confidence_indicators = tone_stats.get('confidence_indicators', 0)
    
    if engagement_score < 2.0:
        feedback['scores']['tone'] = 'low_engagement'
        feedback['recommendations'].append(
            "Your speech could be more engaging. Consider asking questions, using 'you' and 'we', "
            "or varying your sentence structure to connect better with your audience."
        )
    else:
        feedback['scores']['tone'] = 'engaging'
        feedback['recommendations'].append(
            f"Good engagement! Your speech includes questions, direct address, and varied structure."
        )
    
    if confidence_indicators > 0:
        feedback['recommendations'].append(
            f"Great use of confidence indicators! You used {confidence_indicators} confidence-building words/phrases."
        )
    
    # Grammar feedback
    grammar_stats = language_metrics.get('grammar', {})
    issue_count = grammar_stats.get('issue_count', 0)
    
    if issue_count > 0:
        feedback['scores']['grammar'] = 'issues'
        issues = grammar_stats.get('grammar_issues', [])
        if issues:
            feedback['recommendations'].append(
                f"Found {issue_count} potential grammar issue(s): {', '.join(issues[:3])}."
            )
    else:
        feedback['scores']['grammar'] = 'good'
        feedback['recommendations'].append(
            "No obvious grammar issues detected. Your speech is well-structured."
        )
    
    return feedback


def generate_body_language_feedback(body_metrics):
    """
    Generate feedback for body language analysis
    
    Args:
        body_metrics: Dictionary with body language analysis metrics
    
    Returns:
        feedback: Dictionary with scores and recommendations
    """
    feedback = {
        'scores': {},
        'recommendations': []
    }
    
    # Posture feedback
    posture = body_metrics.get('posture', {})
    posture_score = posture.get('posture_score', 0.0)
    slouching = posture.get('slouching_detected', True)
    upright_percentage = posture.get('upright_percentage', 0.0)
    
    if posture_score < 0.5 or slouching:
        feedback['scores']['posture'] = 'poor'
        feedback['recommendations'].append(
            f"Your posture needs improvement (upright {upright_percentage*100:.0f}% of the time). "
            "Stand straight with shoulders back, keep your spine aligned, and avoid slouching. "
            "Good posture conveys confidence and professionalism."
        )
    elif posture_score < 0.7:
        feedback['scores']['posture'] = 'fair'
        feedback['recommendations'].append(
            f"Your posture is decent (upright {upright_percentage*100:.0f}% of the time). "
            "Try to maintain better alignment throughout your presentation for a more confident appearance."
        )
    else:
        feedback['scores']['posture'] = 'good'
        feedback['recommendations'].append(
            f"Excellent posture! You maintained good alignment {upright_percentage*100:.0f}% of the time. "
            "This conveys confidence and professionalism."
        )
    
    # Gesture feedback
    gestures = body_metrics.get('gestures', {})
    gesture_frequency = gestures.get('gesture_frequency', 0.0)
    hands_visible = gestures.get('hands_visible_percentage', 0.0)
    movement_score = gestures.get('hand_movement_score', 0.0)
    
    if hands_visible < 0.3:
        feedback['scores']['gestures'] = 'low'
        feedback['recommendations'].append(
            "Your hands were not visible for most of the presentation. "
            "Use hand gestures to emphasize points and engage your audience. "
            "Keep your hands above your waist and visible to the camera."
        )
    elif gesture_frequency < 0.5:
        feedback['scores']['gestures'] = 'low'
        feedback['recommendations'].append(
            "You used very few gestures. Appropriate hand movements can help emphasize key points "
            "and make your presentation more engaging. Try using gestures to illustrate concepts."
        )
    elif gesture_frequency > 3.0:
        feedback['scores']['gestures'] = 'excessive'
        feedback['recommendations'].append(
            f"You used gestures very frequently ({gesture_frequency:.1f} per second). "
            "While gestures are good, too many can be distracting. Try to use gestures more strategically "
            "to emphasize important points rather than constantly moving your hands."
        )
    else:
        feedback['scores']['gestures'] = 'good'
        feedback['recommendations'].append(
            f"Good use of gestures! You used them at an appropriate frequency ({gesture_frequency:.1f} per second). "
            "Your hand movements help emphasize points and engage the audience."
        )
    
    # Eye contact feedback
    eye_contact = body_metrics.get('eye_contact', {})
    eye_contact_pct = eye_contact.get('eye_contact_percentage', 0.0)
    gaze_direction = eye_contact.get('gaze_direction', 'unknown')
    face_visible = eye_contact.get('face_visible_percentage', 0.0)
    
    if face_visible < 0.5:
        feedback['scores']['eye_contact'] = 'poor'
        feedback['recommendations'].append(
            "Your face was not clearly visible for much of the presentation. "
            "Ensure good lighting and position yourself so your face is clearly visible to the audience."
        )
    elif eye_contact_pct < 0.3:
        feedback['scores']['eye_contact'] = 'poor'
        feedback['recommendations'].append(
            f"You made eye contact only {eye_contact_pct*100:.0f}% of the time. "
            "Try to look directly at the camera/audience more often. Good eye contact builds trust and engagement."
        )
    elif eye_contact_pct < 0.6:
        feedback['scores']['eye_contact'] = 'fair'
        feedback['recommendations'].append(
            f"Your eye contact was moderate ({eye_contact_pct*100:.0f}%). "
            "Try to increase direct eye contact with your audience to build better connection."
        )
    else:
        feedback['scores']['eye_contact'] = 'good'
        feedback['recommendations'].append(
            f"Excellent eye contact! You looked at the audience {eye_contact_pct*100:.0f}% of the time. "
            "This helps build trust and engagement."
        )
    
    # Facial expression feedback
    expressions = body_metrics.get('facial_expressions', {})
    engagement_score = expressions.get('engagement_score', 0.0)
    confidence_score = expressions.get('confidence_score', 0.0)
    smile_pct = expressions.get('smile_percentage', 0.0)
    
    if engagement_score < 0.4:
        feedback['scores']['facial_expressions'] = 'low'
        feedback['recommendations'].append(
            "Your facial expressions showed low engagement. Try to smile more naturally and "
            "show enthusiasm through your expressions. This helps connect with your audience."
        )
    elif engagement_score < 0.6:
        feedback['scores']['facial_expressions'] = 'moderate'
        feedback['recommendations'].append(
            f"Your facial expressions showed moderate engagement ({engagement_score*100:.0f}%). "
            "Try to show more enthusiasm and confidence through natural smiles and expressive eyes."
        )
    else:
        feedback['scores']['facial_expressions'] = 'good'
        feedback['recommendations'].append(
            f"Great facial expressions! You showed good engagement ({engagement_score*100:.0f}%) "
            f"and confidence ({confidence_score*100:.0f}%). Your expressions help connect with the audience."
        )
    
    # Movement feedback
    movement = body_metrics.get('movement', {})
    movement_type = movement.get('movement_type', 'unknown')
    movement_score = movement.get('movement_score', 0.0)
    
    if movement_type == 'stationary':
        feedback['scores']['movement'] = 'stationary'
        feedback['recommendations'].append(
            "You remained very still throughout the presentation. While this can show composure, "
            "some natural movement can make you appear more dynamic and engaging. "
            "Consider subtle shifts in position or leaning slightly forward to emphasize points."
        )
    elif movement_type == 'excessive':
        feedback['scores']['movement'] = 'excessive'
        feedback['recommendations'].append(
            "You moved around quite a bit during the presentation. While movement can be engaging, "
            "excessive movement can be distracting. Try to find a balance - move purposefully "
            "to emphasize points rather than constant shifting."
        )
    else:
        feedback['scores']['movement'] = 'appropriate'
        feedback['recommendations'].append(
            "Good movement! You maintained appropriate body movement that enhances rather than "
            "distracts from your presentation."
        )
    
    # Overall presence feedback
    presence_score = body_metrics.get('presence_score', 0.0)
    
    if presence_score < 0.5:
        feedback['scores']['overall'] = 'needs_improvement'
        feedback['recommendations'].append(
            f"Overall stage presence score: {presence_score*100:.0f}%. Focus on improving posture, "
            "eye contact, and using gestures to enhance your presence."
        )
    elif presence_score < 0.7:
        feedback['scores']['overall'] = 'good'
        feedback['recommendations'].append(
            f"Good overall presence ({presence_score*100:.0f}%)! Continue working on the areas mentioned above "
            "to further improve your stage presence."
        )
    else:
        feedback['scores']['overall'] = 'excellent'
        feedback['recommendations'].append(
            f"Excellent stage presence ({presence_score*100:.0f}%)! You demonstrated strong body language "
            "throughout your presentation."
        )
    
    return feedback

