class Formatter:
    def __str__(self):
        klass = self.__class__.__name__
        values = []

        for value in self.__dict__.items():
            values.append(value)

        if not len(values):
            return '%s/>' % klass

        values = ['\n  %s=%s' % (key, value) for (key, value) in values]

        return '<%s%s\n/>' % (klass, ' '.join(values))
