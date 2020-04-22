import { faArrowRight } from '@fortawesome/free-solid-svg-icons/faArrowRight';
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons/faArrowLeft';
import { faCircle } from '@fortawesome/free-solid-svg-icons/faCircle';
import { faCaretDown } from '@fortawesome/free-solid-svg-icons/faCaretDown';
import { faTimes } from '@fortawesome/free-solid-svg-icons/faTimes';
import { faDownload } from '@fortawesome/free-solid-svg-icons/faDownload';

const iconMap = [
  faArrowRight,
  faArrowLeft,
  faCircle,
  faCaretDown,
  faDownload,
  faTimes,
].reduce((map, obj) => {
  map[obj.iconName] = obj;
  return map;
}, {});

export default iconMap;
