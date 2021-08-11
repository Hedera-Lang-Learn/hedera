import { createLocalVue, mount } from '@vue/test-utils';
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format';

import BookmarkItem from '../app/modules/BookmarkItem.vue';

const localVue = createLocalVue();
localVue.use(VueFilterDateFormat);

describe('BookmarkItem', () => {
  const bookmark = {
    id: 51,
    createdAt: '2021-08-05T22:18:31.872Z',
    text: {
      id: 8,
      userId: 1,
      learnerUrl: '/lemmatized_text/8/learner/',
      title: 'ORATIO IN L. CATILINAM SECVNDA',
    },
  };

  const createdAtMachineReadable = bookmark.createdAt.substr(0, 10); // YYYY-MM-DD

  it('loads in BookmarkItem', () => {
    const wrapper = mount(BookmarkItem, {
      propsData: { bookmark },
      localVue,
    });
    expect(wrapper.classes('bookmark-item'))
      .toBe(true);
  });

  it('links back to the text', () => {
    const wrapper = mount(BookmarkItem, {
      propsData: { bookmark },
      localVue,
    });
    const anchorEl = wrapper.find('a');
    expect(anchorEl.exists()).toBe(true);
    expect(anchorEl.attributes('href')).toEqual(bookmark.text.learnerUrl);
  });

  it('shows the created at date', () => {
    const wrapper = mount(BookmarkItem, {
      propsData: { bookmark },
      localVue,
    });
    const timeEl = wrapper.find('time');
    expect(timeEl.exists()).toBe(true);
    expect(timeEl.attributes('datetime')).toEqual(createdAtMachineReadable);
  });
});
