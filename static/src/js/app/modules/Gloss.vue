<template>
    <div v-if="gloss" class="gloss" :class="highlighted ? 'gloss--highlighted' : ''">
      <label :for="checkbox_id" class="gloss__label">
        <input :id="checkbox_id" class="input_checkbox" type="checkbox" :checked="highlighted" @click="onClickCheckBox">
        <span id="checked" class="checkbox"></span>
      </label>
      <p>{{gloss.gloss}}</p>
    </div>
</template>
<script>

  export default {
    name: 'Gloss',
    props: ['gloss', 'highlighted'],
    data() {
      console.log('gloss', this.gloss, this.highlighted);
      return {
        checkbox_id: `gloss-${this.gloss.pk}`,
      };
    },
    methods: {
      onClick(e) {
        console.log(e);
        this.$emit('selected', this.gloss);
      },
      onClickCheckBox(e) {
        console.log('clicked checkbox', e);
        this.highlighted = !this.highlighted;
      },
    },
  };
</script>

<style lang="scss">
@import "../../../scss/config";
.gloss {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 16px;
}
.gloss--highlighted {
  background-color: $highlight-color;
}
.gloss__label {
  display: flex;
  margin: 0;
  width: 30px;
  height: 30px;
  cursor: pointer;
}
.input_checkbox {
  position: absolute;
  transform: scale(0);
}
input:checked ~ .checkbox {
  transform: rotate(45deg);
  width: 20px;
  margin: -5px 7px 0 8px;
  border-color: $hedera-green;
  border-width: 4px;
  border-top-color: transparent;
  border-left-color: transparent;
  border-radius: 0;
}
.checkbox {
  display: block;
  width: inherit;
  height: inherit;
  border: 2px solid #999;
  border-radius: 4px;
  transition: all 0.2s cubic-bezier(0, 0.01, 0.23, 0.8);
}

//.gloss {
//  cursor: pointer;
//  text-indent: 2em;
//  font-style: italic;
//  color: $gray-600;
//  font-size: 11pt;
//  padding: 4px;
//  &:hover {
//    background-color: $highlight-color;
//  }
//}
</style>
