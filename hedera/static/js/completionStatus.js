const updatePage = (lemma, length) => {
  const teacher = document.createElement('a');
  const learner = document.createElement('a');
  const clone = document.createElement('a');
  const cloneIcon = document.createElement('icon');
  const teacherText = document.createTextNode('Teacher');
  const learnerText = document.createTextNode('Learner');
  const cloneText = document.createTextNode('Clone');
  const lengthText = document.createTextNode(length);
  teacher.appendChild(teacherText);
  learner.appendChild(learnerText);
  teacher.href = `/lemmatized_text/${lemma}/`;
  learner.href = `/lemmatized_text/${lemma}/learner/`;
  clone.href = `/lemmatized_text/create/?cloned_from=${lemma}`;
  clone.classList.add('btn', 'btn-outline-primary', 'btn-sm');
  cloneIcon.classList.add('fa', 'fa-copy');
  const title = document.getElementById(`title-${lemma}`);
  title.appendChild(document.createElement('br'));
  title.appendChild(teacher);
  title.appendChild(document.createTextNode(' \u2022 '));
  title.appendChild(learner);
  const progressDiv = document.getElementById(`progress-${lemma}`);
  const progressDivParent = progressDiv.parentNode;
  progressDivParent.removeChild(progressDiv);
  progressDivParent.appendChild(lengthText);
  clone.appendChild(cloneIcon);
  clone.appendChild(cloneText);
  const buttonColumn = document.getElementById(`button-column-${lemma}`);
  buttonColumn.appendChild(clone);
};


const fetchStatus = (lemma) => {
  window.fetch(`${window.location.href}${lemma}/status/`)
    .then(r => r.json())
    .then((rj) => {
      const bar = document.getElementById(lemma);
      bar.setAttribute('aria-valuenow', rj.status);
      bar.setAttribute('style', `width: ${rj.status}%`);
      if (rj.status !== 100) {
        setTimeout(fetchStatus, 5000, lemma);
      } else {
        updatePage(lemma, rj.len);
      }
    });
};

const lemmatizedTexts = document.getElementsByClassName('progress-bar');
const barIds = Array.prototype.map.call(lemmatizedTexts, lemma => lemma.id);

barIds.forEach((lemma) => {
  fetchStatus(lemma);
});
