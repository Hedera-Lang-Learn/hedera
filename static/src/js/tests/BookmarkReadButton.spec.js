import { createLocalVue, mount } from '@vue/test-utils';
import Vuex from 'vuex';

import { BOOKMARK_READ_UPDATE } from '../app/constants';
import BookmarkReadButton from '../app/modules/BookmarkReadButton.vue';

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
    readStatus: true,
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
    readStatus: false,
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

describe('BookmarkReadButton', () => {
  const bookmarks = bookmarksFixture();
  let actions;
  let store;

  const mountComponent = ({ textId }) => mount(BookmarkReadButton, {
    propsData: { textId },
    store,
    localVue,
  });

  beforeEach(() => {
    actions = {
      [BOOKMARK_READ_UPDATE]: jest.fn(),
    };
    store = new Vuex.Store({
      state: { bookmarks },
      actions,
    });
  });

  it('loads in BookmarkReadButton', () => {
    const textId = bookmarks[0].text.id;
    const wrapper = mountComponent({ textId });
    expect(wrapper.element.tagName).toEqual('BUTTON');
  });

  it('shows Mark as Read if the text has not been read', () => {
    const textId = bookmarks[1].text.id;
    const wrapper = mountComponent({ textId });
    expect(wrapper.text().trim()).toEqual('Mark as Read');
  });

  it('shows Mark as Unread if the text has been read', () => {
    const textId = bookmarks[0].text.id;
    const wrapper = mountComponent({ textId });
    expect(wrapper.text().trim()).toEqual('Mark as Unread');
  });

  it('marks the bookmark as read when the button is pressed and the text is not read', async () => {
    const textId = bookmarks[1].text.id;
    const wrapper = mountComponent({ textId });
    const button = wrapper.find('button');
    await button.trigger('click.prevent');

    expect(actions[BOOKMARK_READ_UPDATE]).toHaveBeenCalled();
  });

  it('marks the bookmark as unread when the button is pressed and the text is read', async () => {
    const textId = bookmarks[0].text.id;
    const wrapper = mountComponent({ textId });
    const button = wrapper.find('button');
    await button.trigger('click.prevent');

    expect(actions[BOOKMARK_READ_UPDATE]).toHaveBeenCalled();
  });
});
