<template>
    <div class="lattice-tree">
        <h4>{{ token.token }}</h4>

        <LatticeNode :node="node" v-if="node" />
        <div v-else>
            No Lemma
        </div>
    </div>
</template>
<script>
import LatticeNode from './LatticeNode.vue';

export default {
    props: ['token', 'index', 'node'],
    components: { LatticeNode },
}
</script>
