import { shallowMount } from '@vue/test-utils';
import Dashboard from '../app/Dashboard.vue';

describe('Dashboard', () => {
  it('loads in dashboard', () => {
    const wrapper = shallowMount(Dashboard);
    expect(wrapper.classes('dashboard')).toBe(true);
  });
});
