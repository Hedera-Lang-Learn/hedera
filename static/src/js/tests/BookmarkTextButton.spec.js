import { createLocalVue, mount } from '@vue/test-utils';
import Vuex from 'vuex';

import { ADD_BOOKMARK, REMOVE_BOOKMARK } from '../app/constants';
import BookmarkTextButton from '../app/modules/BookmarkTextButton.vue';

const localVue = createLocalVue();
localVue.use(Vuex);

const bookmarksFixture = () => [
  {
    id: 85,
    userId: 1,
    createdAt: '2021-08-11T20:39:51.833Z',
    text: {
      id: 2,
      title: 'C. Julius Caesar, De bello Gallico - Section 2',
      lang: 'lat',
      learnerUrl: '/lemmatized_text/2/learner/',
    },
  },
  {
    id: 84,
    userId: 1,
    createdAt: '2021-08-11T20:39:48.476Z',
    text: {
      id: 1,
      title: 'C. Julius Caesar, De bello Gallico - Section 1',
      lang: 'lat',
      learnerUrl: '/lemmatized_text/1/learner/',
    },
  },
  {
    id: 50,
    userId: 1,
    createdAt: '2021-08-05T22:11:13.107Z',
    text: {
      id: 3,
      title: 'From Homer\'s Odyssey',
      lang: 'grc',
      learnerUrl: '/lemmatized_text/3/learner/',
    },
  },
];

describe('BookmarkTextButton', () => {
  const bookmarks = bookmarksFixture();
  const textIdNotInBookmarks = Math.max(...bookmarks.map((b) => b.text.id)) + 1;
  let actions;
  let store;

  const mountComponent = ({ textId }) => mount(BookmarkTextButton, {
    propsData: { textId },
    store,
    localVue,
  });

  beforeEach(() => {
    actions = {
      [ADD_BOOKMARK]: jest.fn(),
      [REMOVE_BOOKMARK]: jest.fn(),
    };
    store = new Vuex.Store({
      state: { bookmarks },
      actions,
    });
  });

  it('loads in BookmarkTextButton', () => {
    const textId = bookmarks[0].text.id;
    const wrapper = mountComponent({ textId });
    expect(wrapper.element.tagName).toEqual('BUTTON');
  });

  it('shows Add Bookmark if the text has not been bookmarked', () => {
    const textId = textIdNotInBookmarks;
    const wrapper = mountComponent({ textId });
    expect(wrapper.text().trim()).toEqual('Add Bookmark');
  });

  it('shows Remove Bookmark if the text has been bookmarked', () => {
    const textId = bookmarks[0].text.id;
    const wrapper = mountComponent({ textId });
    expect(wrapper.text().trim()).toEqual('Remove Bookmark');
  });

  it('adds the bookmark when the button is pressed and the text is not bookmarked', async () => {
    const textId = textIdNotInBookmarks;
    const wrapper = mountComponent({ textId });
    const button = wrapper.find('button');
    await button.trigger('click.prevent');

    expect(actions[ADD_BOOKMARK]).toHaveBeenCalled();
  });

  it('removes the bookmark when the button is pressed and the text is not bookmarked', async () => {
    const textId = bookmarks[0].text.id;
    const wrapper = mountComponent({ textId });
    const button = wrapper.find('button');
    await button.trigger('click.prevent');

    expect(actions[REMOVE_BOOKMARK]).toHaveBeenCalled();
  });
});
