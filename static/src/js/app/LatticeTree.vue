<template>
    <div class="lattice-tree">
        <h4>{{ token.token }}</h4>

        <LatticeNode :node="node" @selected="onSelect" v-if="node" />
        <div v-else>
            No Lemma
        </div>
    </div>
</template>
<script>
import LatticeNode from './LatticeNode.vue';
import { UPDATE_TOKEN } from './constants';

export default {
    props: ['token', 'index', 'node'],
    components: { LatticeNode },
    methods: {
        onSelect(node) {
            const textId = this.$route.params.id;
            this.$store.dispatch(UPDATE_TOKEN, {
                id: textId,
                tokenIndex: this.index,
                nodeId: node.pk
            });
        }
    }
}
</script>
