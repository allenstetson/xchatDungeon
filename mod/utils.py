__module_name__ = 'dnd.utils'
__module_version__ = '1.0'
__module_description__ = 'Common Utilities'
__module_author__ = 'Allen Stetson'

class ProbabilityArray(object):
    def create(self, inputs):
        """
        This takes a hash table with a key and a value that represents its probability of being
        chosen (or more to the point, its frequency)
        Here we will create an array the size of the total probability, and we'll pack into that
        array the formulas provided, packing them the number of times defined by their probability.
        For instance, if formula A had a probability of 5, B=2, C=1, our resulting array would equal:
        A,A,A,A,A,B,B,C
        """
        allItems = []
        for itemSet in inputs:
          (item, weight) = itemSet
          for instance in range(weight):
            allItems.append(item)
        return allItems

class ArticleDeterminer(object):
    def determine(self, word):
        # Article
        article = 'a'
        if word[0].lower() in ['a','e','i','o','u']:
            article = 'an'
        return(article)