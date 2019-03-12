<template>
    <div>
        {{ words }}
    </div>
</template>
<script>
export default {
    props: ['vocabList'],
    computed: {
        words() {
            return this.vocabList.words;
        }
    }
}
</script>
