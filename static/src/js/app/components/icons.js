import { faArrowRight } from '@fortawesome/free-solid-svg-icons/faArrowRight';
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons/faArrowLeft';
import { faCircle } from '@fortawesome/free-solid-svg-icons/faCircle';

const iconMap = [
  faArrowRight,
  faArrowLeft,
  faCircle,
].reduce((map, obj) => {
  map[obj.iconName] = obj;
  return map;
}, {});

export default iconMap;
