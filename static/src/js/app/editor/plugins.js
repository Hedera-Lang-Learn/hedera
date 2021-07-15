export default function ConvertSpanAttributes(editor) {
  // Allow <span> elements in the model.
  editor.model.schema.register('span', {
    allowWhere: '$block',
    allowContentOf: '$root',
  });
  // The view-to-model converter converting a view <span> with all its attributes to the model.
  editor.conversion.for('upcast').elementToElement({
    view: 'span',
    model: (viewElement, { writer: modelWriter }) => modelWriter.createElement('span', viewElement.getAttributes()),
  });
  // The model-to-view converter for the <span> element (attributes are converted separately).
  editor.conversion.for('downcast').elementToElement({
    model: 'span',
    view: 'span',
  });
  // The model-to-view converter for <span> attributes.
  // Note that a lower-level, event-based API is used here.
  editor.conversion.for('downcast').add((dispatcher) => {
    dispatcher.on('attribute', (evt, data, conversionApi) => {
      // Convert <span> attributes only.
      if (data.item.name !== 'span') {
        return;
      }

      const viewWriter = conversionApi.writer;
      const viewSpan = conversionApi.mapper.toViewElement(data.item);

      // In the model-to-view conversion we convert changes.
      // An attribute can be added or removed or changed.
      // The below code handles all 3 cases.
      if (data.attributeNewValue) {
        viewWriter.setAttribute(data.attributeKey, data.attributeNewValue, viewSpan);
      } else {
        viewWriter.removeAttribute(data.attributeKey, viewSpan);
      }
    });
  });
}
