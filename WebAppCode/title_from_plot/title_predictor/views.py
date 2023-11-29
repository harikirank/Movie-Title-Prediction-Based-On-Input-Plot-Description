import gensim
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, Context
from gensim.models import Doc2Vec
from django.templatetags.static import static
from django.shortcuts import redirect
from .forms.plot_input_form import TitlePredictionForm
from django.contrib.staticfiles.storage import staticfiles_storage

# Create your views here.
model_path = "A:\Fall 2023\Information Retrieval and WebSearch\Project\Project Final\Website Code\\title_from_plot\\title_predictor\static\\title_predictor\doc2vec_whole_data_set.model"
df = pd.read_csv(
    "A:\Fall 2023\Information Retrieval and WebSearch\Project\Project Final\Website Code\\title_from_plot\\title_predictor\static\\title_predictor\wiki_movie_plots_deduped.csv",
    sep=",")
doc2vec_model = Doc2Vec.load(model_path)


class Movie:
    def __init__(self):
        pass


def title_prediction(request):
    if request.method == 'POST':
        pred_form = TitlePredictionForm(request.POST)
        if pred_form.is_valid():
            # Make the prediction and show the user the list of predictions with scores.
            # model_path = static('title_predictor/wiki_movie_plots_deduped.css')

            input_plot = gensim.parsing.preprocessing.preprocess_string(request.POST.get("plot", ""))
            test_doc_vector = doc2vec_model.infer_vector(input_plot)
            sims = doc2vec_model.docvecs.most_similar(positive=[test_doc_vector])

            predictions = []
            for s in sims:
                tmp_movie = [df['Title'].iloc[s[0]], str(round(s[1], 2)), df['Plot'].iloc[s[0]], df['Genre'].iloc[s[0]],
                             df['Origin/Ethnicity'].iloc[s[0]], str(df['Release Year'].iloc[s[0]])]
                predictions.append(tmp_movie)

                # predictions.append(f"{df['Title'].iloc[s[0]]} has a match with similarity: { s[1] }")

            request.session['predictions'] = predictions

            return redirect('/success/', predictions)
        else:
            # show the form with the errors
            return render(
                request,
                'title_predictor/title_prediction.html',
                {'form': pred_form})
    else:
        form = TitlePredictionForm()
        return render(
            request,
            'title_predictor/title_prediction.html',
            {'form': form})

    # template = loader.get_template('title_predictor/title_prediction.html')
    #
    # context = {'name': 'Hari Kiran Keerthipati'}
    # return HttpResponse(template.render(context))


def show_results(request):
    predictions = request.session.get('predictions')
    print(f"The preds are: {predictions}")
    return render(
        request,
        'title_predictor/show_predictions.html',
        {'predictions': predictions})
