<template>
    <div v-if="gloss" :class="active ? 'gloss gloss--active' : 'gloss'">
      <label :for="labelIdentifier" class="gloss__label">
        <input :id="labelIdentifier" type="checkbox" :checked="active" @change="onChange">
        <span class="checkbox"></span>
        <p>{{gloss.gloss}}</p>
      </label>
    </div>
</template>
<script>

  export default {
    name: 'Gloss',
    props: ['gloss', 'active'],
    data() {
      console.log('Gloss data', this.gloss.pk, 'active', this.active);
      return {
        labelIdentifier: `gloss-${this.gloss.pk}`,
      };
    },
    methods: {
      onChange(e) {
        this.$emit('change', this.gloss, e.target.checked);
      },
    },
  };
</script>

<style lang="scss">
@import "../../../scss/config";
.gloss {
  margin: 0;
  padding-left: 32px;
  padding-top: 4px;
  &:hover {
    background-color: #d3d3d3;
  }
  p {
    margin-left: 16px;
    flex-grow: 1;
    width: 100%;
  }
  input {
    position: absolute;
    transform: scale(0);
  }
  input:checked ~ .checkbox {
    transform: rotate(45deg);
    width: 20px;
    margin: -5px 7px 0 8px;
    border-color: #fff;
    border-width: 4px;
    border-top-color: transparent;
    border-left-color: transparent;
    border-radius: 0;
  }
  .checkbox {
    display: block;
    width: 30px;
    height: 30px;
    border: 2px solid #999;
    border-radius: 4px;
    transition: all 0.2s cubic-bezier(0, 0.01, 0.23, 0.8);
    flex-shrink: 0;
    flex-grow: 0;
  }
  input:checked + .checkbox + p {
    color: #fff;
  }
}
.gloss--active {
  background-color: #80b180;
}
.gloss__label {
  display: flex;
  margin: 0;
  padding: 0;
  cursor: pointer;
}
</style>
