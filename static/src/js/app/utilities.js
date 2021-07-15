export const transormTokensToEditableHTML (tokens) => (
  tokens.map((token) => (
    `<span
      node=${token.node}
      resolved=${token.resolved}
      previously-lemmatized="true"
    >
    ${token.word}
    </span>`
  )).join('')
);

// `${token.following ? `<span class="following" >${token.following}</span>` : ``}`

export const anotherFunction = () => 0;
