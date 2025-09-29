export const DATE_FORMAT_OPTIONS = {
  locale: "en-US",
  options: {
    year: "numeric",
    month: "long",
    day: "numeric"
  }
};

export const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString(
    DATE_FORMAT_OPTIONS.locale
  );
};
 
export const formatDateDetailed = (dateString) => {
  return new Date(dateString).toLocaleDateString(
    DATE_FORMAT_OPTIONS.locale,
    DATE_FORMAT_OPTIONS.options
  );
};