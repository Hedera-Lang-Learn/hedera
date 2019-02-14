<template>
    <div class="lattice-tree">
        <h4>{{ token.token }}</h4>

        <LatticeNode :node="node" @selected="onSelect" v-if="node" />
        <div v-else>
            No Lemma
        </div>

        <a href="" @click.prevent="markResolved(!token.resolved)">Mark {{ token.resolved ? 'Unresolved' : 'Resolved '}}</a>
    </div>
</template>
<script>
import LatticeNode from './LatticeNode.vue';
import { UPDATE_TOKEN } from './constants';

export default {
    props: ['token', 'index', 'node'],
    components: { LatticeNode },
    computed: {
        textId() {
            return this.$route.params.id;
        }
    },
    methods: {
        onSelect(node) {
            this.$store.dispatch(UPDATE_TOKEN, {
                id: this.textId,
                tokenIndex: this.index,
                nodeId: node.pk,
                resolved: this.token.resolved,
            });
        },
        markResolved(resolved) {
            this.$store.dispatch(UPDATE_TOKEN, {
                id: this.textId,
                tokenIndex: this.index,
                nodeId: this.node ? this.node.pk : null,
                resolved: resolved,
            });
        }
    }
}
</script>
