import { shallowMount } from '@vue/test-utils';
import LatticeNode from '../app/modules/LatticeNode.vue';

describe('LatticeNode', () => {
  it('loads in LatticeNode', () => {
    const wrapper = shallowMount(LatticeNode);
    // TODO ADD BETTER TEST
    expect(wrapper).toBe(wrapper);
  });
});
