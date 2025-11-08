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

