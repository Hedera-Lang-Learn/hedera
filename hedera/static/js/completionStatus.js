const updatePage = (lemma, length) => {
  let teacher = document.createElement("a");
  let learner = document.createElement("a");
  let clone = document.createElement("a");
  let cloneIcon = document.createElement("icon");
  let teacherText = document.createTextNode("Teacher");
  let learnerText = document.createTextNode("Learner");
  let cloneText = document.createTextNode("Clone");
  let lengthText = document.createTextNode(length);
  teacher.appendChild(teacherText);
  learner.appendChild(learnerText);
  teacher.href = '/lemmatized_text/' + lemma + '/';
  learner.href = '/lemmatized_text/' + lemma + '/learner/';
  clone.href = '/lemmatized_text/create/?cloned_from=' + lemma;
  clone.classList.add('btn', 'btn-outline-primary', 'btn-sm');
  cloneIcon.classList.add('fa', 'fa-copy');
  let title = document.getElementById('title-' + lemma)  
  title.appendChild(document.createElement("br"));
  title.appendChild(teacher);
  title.appendChild(document.createTextNode(' \u2022 '));
  title.appendChild(learner);
  let progressDiv = document.getElementById('progress-' + lemma);
  let progressDivParent = progressDiv.parentNode;
  progressDivParent.removeChild(progressDiv);
  progressDivParent.appendChild(lengthText);
  clone.appendChild(cloneIcon);
  clone.appendChild(cloneText);
  let buttonColumn = document.getElementById('button-column-' + lemma);
  buttonColumn.appendChild(clone);
}


const fetchStatus = lemma => {
  window.fetch(window.location.href + lemma + '/status/')
    .then( r => {
      return r.json();
    })
    .then( rj => {
      let bar = document.getElementById(lemma);
      bar.setAttribute('aria-valuenow', rj['status']);
      bar.setAttribute('style', "width: " + rj['status'] + "%");
      if(rj['status'] !== 100){
        setTimeout(fetchStatus, 5000, lemma);
      } else {
        updatePage(lemma, rj['length']);         
      }
    });
}

const lemmatizedTexts =  document.getElementsByClassName('progress-bar');
let barIds = Array.prototype.map.call(lemmatizedTexts, (lemma) => lemma.id);

barIds.forEach( lemma => {
  fetchStatus(lemma);
});
